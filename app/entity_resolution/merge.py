import uuid
from typing import List
from app.entity_resolution.schemas import EntityBase

class EntityMerger:
    @staticmethod
    def _merge_lists(lists: List[List[str]]) -> List[str]:
        merged_set = set()
        for lst in lists:
            if lst:
                for item in lst:
                    if item:
                        merged_set.add(item.strip())
        return sorted(list(merged_set))

    @classmethod
    def merge(cls, entity1: EntityBase, entity2: EntityBase) -> EntityBase:
        # Determine the canonical base (prefer the one with higher confidence)
        base, other = (entity1, entity2) if entity1.confidence_score >= entity2.confidence_score else (entity2, entity1)
        
        # Merge scalar fields (prefer base, fallback to other)
        merged_data = {
            "id": base.id, # Keep base ID
            "company_name": base.company_name or other.company_name,
            "website": base.website or other.website,
            "location": base.location or other.location,
            "industry": base.industry or other.industry,
            "description": base.description or other.description,
            "confidence_score": max(base.confidence_score, other.confidence_score)
        }
        
        # Merge list fields uniquely
        merged_data["founders"] = cls._merge_lists([base.founders, other.founders])
        merged_data["products"] = cls._merge_lists([base.products, other.products])
        merged_data["technologies"] = cls._merge_lists([base.technologies, other.technologies])
        merged_data["keywords"] = cls._merge_lists([base.keywords, other.keywords])
        
        return EntityBase(**merged_data)
