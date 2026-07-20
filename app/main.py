from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ingestion, entity_resolution, validation, export, llm
from app.database.database import engine, Base
from app.database import models

app = FastAPI(title="AI Data Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion.router)
app.include_router(llm.router, prefix="/llm", tags=["LLM Extraction"])
app.include_router(entity_resolution.router, prefix="/entity-resolution", tags=["Entity Resolution"])
app.include_router(validation.router, prefix="/validation", tags=["Validation"])
app.include_router(export.router, prefix="/export", tags=["Export"])

@app.on_event("startup")
async def startup_event():
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("app")
    logger.info("Starting AI Data Intelligence Platform")
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown_event():
    import logging
    logger = logging.getLogger("app")
    logger.info("Shutting down AI Data Intelligence Platform")
