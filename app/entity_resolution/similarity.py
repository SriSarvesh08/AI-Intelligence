from difflib import SequenceMatcher
from typing import Tuple, List
from app.entity_resolution.schemas import EntityBase
from app.entity_resolution.normalizer import EntityNormalizer

class SimilarityEngine:
    
    @staticmethod
    def _string_similarity(a: str, b: str) -> float:
        if not a and not b:
            return 0.0
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def _list_similarity(list_a: List[str], list_b: List[str]) -> float:
        if not list_a and not list_b:
            return 0.0
        if not list_a or not list_b:
            return 0.0
            
        # Very basic list overlap similarity
        norm_a = set(EntityNormalizer.normalize_name(x) for x in list_a)
        norm_b = set(EntityNormalizer.normalize_name(x) for x in list_b)
        
        intersection = len(norm_a.intersection(norm_b))
        union = len(norm_a.union(norm_b))
        
        return intersection / union if union > 0 else 0.0

    @classmethod
    def compare(cls, entity1: EntityBase, entity2: EntityBase) -> Tuple[float, List[str]]:
        reasons = []
        scores = []
        weights = []

        # 1. Company Name Comparison (Highest Weight)
        if entity1.company_name and entity2.company_name:
            norm1 = EntityNormalizer.normalize_company_name(entity1.company_name)
            norm2 = EntityNormalizer.normalize_company_name(entity2.company_name)
            
            score = cls._string_similarity(norm1, norm2)
            scores.append(score)
            weights.append(0.5)
            
            if score > 0.9:
                reasons.append(f"Strong name match ({score:.2f})")
            elif score > 0.7:
                reasons.append(f"Partial name match ({score:.2f})")

        # 2. Website Comparison
        if entity1.website and entity2.website:
            url1 = EntityNormalizer.normalize_url(entity1.website)
            url2 = EntityNormalizer.normalize_url(entity2.website)
            
            if url1 and url2 and url1 == url2:
                scores.append(1.0)
                weights.append(0.3)
                reasons.append("Exact website match")
            else:
                score = cls._string_similarity(url1, url2)
                scores.append(score)
                weights.append(0.3)

        # 3. Founders Comparison
        if entity1.founders and entity2.founders:
            score = cls._list_similarity(entity1.founders, entity2.founders)
            if score > 0:
                scores.append(score)
                weights.append(0.2)
                if score > 0.5:
                    reasons.append(f"Founders overlap ({score:.2f})")

        # If no fields to compare, return 0
        if not scores:
            return 0.0, []

        # Calculate weighted average
        total_weight = sum(weights)
        weighted_score = sum(s * w for s, w in zip(scores, weights)) / total_weight

        return weighted_score, reasons
