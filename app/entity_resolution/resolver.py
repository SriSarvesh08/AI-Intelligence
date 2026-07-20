from typing import List
from app.entity_resolution.schemas import EntityBase, DuplicateCandidate
from app.entity_resolution.similarity import SimilarityEngine
import re
import difflib

# Phase IV: Map extracted entities against a seed list of known canonical entities (mock a small database of 50 known AI startups).
CANONICAL_SEED_LIST = [
    "OpenAI", "Anthropic", "DeepMind", "Hugging Face", "Cohere", "Mistral AI", 
    "Perplexity AI", "Midjourney", "Stability AI", "Scale AI", "Glean", "Adept", 
    "Runway", "Inflection AI", "Databricks", "SambaNova", "CoreWeave", "Together AI",
    "Character.ai", "AI21 Labs", "Anyscale", "Weights & Biases", "Snorkel AI", "Pinecone",
    "Weaviate", "Milvus", "Qdrant", "Chroma", "LangChain", "LlamaIndex", "Haystack",
    "MosaicML", "Nomic AI", "Arthur AI", "Arize AI", "Fiddler AI", "Truera", "Galileo",
    "Tome", "Jasper", "Copy.ai", "Writer", "Typeface", "Descript", "Synthesia",
    "ElevenLabs", "Murf AI", "Pika Labs", "HeyGen", "Rosebud AI"
]

class EntityResolver:
    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold
        # Normalize seed list for case-insensitive and punctuation-free matching
        self.canonical_map = {self._normalize(name): name for name in CANONICAL_SEED_LIST}

    def _normalize(self, text: str) -> str:
        """Strip punctuation and whitespace, lowercase"""
        if not text:
            return ""
        text = text.lower()
        # Remove common corporate suffixes
        text = re.sub(r'\b(inc\.|inc|llc|ltd|corp|corporation)\b', '', text)
        return re.sub(r'[^a-z0-9]', '', text)

    def resolve_canonical_name(self, raw_name: str) -> str:
        """Map extracted entity against the seed list of canonical entities."""
        if not raw_name:
            return raw_name
            
        norm_raw = self._normalize(raw_name)
        
        # 1. Exact normalized match
        if norm_raw in self.canonical_map:
            return self.canonical_map[norm_raw]
            
        # 2. Fuzzy match against seed list
        matches = difflib.get_close_matches(norm_raw, self.canonical_map.keys(), n=1, cutoff=0.85)
        if matches:
            return self.canonical_map[matches[0]]
            
        # 3. Fallback to original raw name if no canonical mapping is found
        return raw_name

    def detect_candidates(self, entities: List[EntityBase]) -> List[DuplicateCandidate]:
        candidates = []
        n = len(entities)
        
        # O(N^2) comparison for demonstration (in production, use blocking/LSH)
        for i in range(n):
            for j in range(i + 1, n):
                entity1 = entities[i]
                entity2 = entities[j]
                
                # Apply Phase IV Canonical Mapping before similarity comparison
                if entity1.company_name:
                    entity1.company_name = self.resolve_canonical_name(entity1.company_name)
                if entity2.company_name:
                    entity2.company_name = self.resolve_canonical_name(entity2.company_name)
                
                score, reasons = SimilarityEngine.compare(entity1, entity2)
                
                if score >= self.threshold:
                    candidates.append(
                        DuplicateCandidate(
                            entity1_id=entity1.id,
                            entity2_id=entity2.id,
                            entity1=entity1,
                            entity2=entity2,
                            similarity_score=score,
                            match_reasons=reasons
                        )
                    )
                    
        # Sort candidates by highest score first
        candidates.sort(key=lambda x: x.similarity_score, reverse=True)
        return candidates
