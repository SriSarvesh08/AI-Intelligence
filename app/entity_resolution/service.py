from typing import List, Dict
import uuid
from app.entity_resolution.schemas import EntityBase, DuplicateCandidate, MergePreview, ResolutionStats
from app.entity_resolution.resolver import EntityResolver
from app.entity_resolution.merge import EntityMerger

# In-memory store for demonstration purposes
MOCK_ENTITIES = [
    EntityBase(
        id=str(uuid.uuid4()),
        company_name="Google Inc.",
        website="https://www.google.com/",
        founders=["Larry Page", "Sergey Brin"],
        location="Mountain View, CA",
        confidence_score=0.95
    ),
    EntityBase(
        id=str(uuid.uuid4()),
        company_name="Google",
        website="google.com",
        founders=["L. Page", "S. Brin"],
        products=["Search", "Ads"],
        confidence_score=0.85
    ),
    EntityBase(
        id=str(uuid.uuid4()),
        company_name="OpenAI LLC",
        website="https://openai.com",
        founders=["Sam Altman", "Greg Brockman", "Ilya Sutskever"],
        location="San Francisco, CA",
        confidence_score=0.99
    ),
    EntityBase(
        id=str(uuid.uuid4()),
        company_name="Open AI",
        website="openai.com",
        founders=["Sam Altman"],
        products=["ChatGPT", "DALL-E"],
        confidence_score=0.88
    ),
    EntityBase(
        id=str(uuid.uuid4()),
        company_name="Anthropic",
        website="https://anthropic.com",
        founders=["Dario Amodei", "Daniela Amodei"],
        products=["Claude"],
        confidence_score=0.96
    )
]

class ResolutionService:
    def __init__(self):
        self.entities = MOCK_ENTITIES.copy()
        self.resolver = EntityResolver(threshold=0.6)
        self.initial_count = len(self.entities)
        self.duplicates_removed = 0

    def get_candidates(self) -> List[MergePreview]:
        candidates = self.resolver.detect_candidates(self.entities)
        previews = []
        for candidate in candidates:
            merged = EntityMerger.merge(candidate.entity1, candidate.entity2)
            previews.append(MergePreview(candidate=candidate, merged_entity=merged))
        return previews

    def apply_merge(self, entity1_id: str, entity2_id: str) -> EntityBase:
        entity1 = next((e for e in self.entities if e.id == entity1_id), None)
        entity2 = next((e for e in self.entities if e.id == entity2_id), None)

        if not entity1 or not entity2:
            raise ValueError("Entities not found")

        merged = EntityMerger.merge(entity1, entity2)
        
        # Remove old entities and add merged
        self.entities = [e for e in self.entities if e.id not in (entity1_id, entity2_id)]
        self.entities.append(merged)
        self.duplicates_removed += 1
        
        return merged

    def get_stats(self) -> ResolutionStats:
        avg_conf = sum(e.confidence_score for e in self.entities) / len(self.entities) if self.entities else 0.0
        
        return ResolutionStats(
            entities_before=self.initial_count,
            entities_after=len(self.entities),
            duplicates_removed=self.duplicates_removed,
            average_confidence=avg_conf
        )

# Global instance for state
resolution_service = ResolutionService()
