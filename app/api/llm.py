from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import json
from app.llm.extractor import ExtractorPipeline

router = APIRouter()
extractor = ExtractorPipeline()

class ExtractionRequest(BaseModel):
    text: str
    source_url: str

@router.post("/extract")
async def extract_data(req: ExtractionRequest):
    async def generate():
        async for progress in extractor.extract_stream(req.text, req.source_url):
            yield f"{json.dumps(progress)}\n"
            
    return StreamingResponse(generate(), media_type="application/x-ndjson")
