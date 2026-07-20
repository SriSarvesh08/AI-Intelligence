from fastapi import APIRouter
from app.entity_resolution.service import resolution_service

router = APIRouter()

@router.post("")
@router.post("/")
async def run_entity_resolution():
    # Detect candidates and apply merges automatically for the endpoint
    candidates = resolution_service.get_candidates()
    for candidate in candidates:
        resolution_service.apply_merge(
            candidate.candidate.entity1.id, 
            candidate.candidate.entity2.id
        )
    
    stats = resolution_service.get_stats()
    return {
        "message": "Entity resolution completed",
        "stats": {
            "entities_before": stats.entities_before,
            "entities_after": stats.entities_after,
            "duplicates_removed": stats.duplicates_removed,
            "average_confidence": stats.average_confidence
        }
    }
