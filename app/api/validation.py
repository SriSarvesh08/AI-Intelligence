from fastapi import APIRouter
from app.validation.validator import DataValidator
from app.entity_resolution.service import resolution_service

router = APIRouter()
validator = DataValidator()

@router.post("")
@router.post("/")
async def validate_data():
    entities = resolution_service.entities
    _, summary = validator.validate_entities(entities)
    return summary.model_dump()
