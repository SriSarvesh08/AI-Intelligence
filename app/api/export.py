from fastapi import APIRouter
import os
from app.export.exporter import DataExporter
from app.entity_resolution.service import resolution_service

router = APIRouter()

@router.post("/json")
async def export_json():
    entities = resolution_service.entities
    json_data = DataExporter.export_to_json(entities)
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "resolved_entities.json")
    with open(file_path, "w") as f:
        f.write(json_data)
        
    return {"message": "Exported to output/resolved_entities.json successfully"}
