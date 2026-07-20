import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.ingestion import IngestionConfig, IngestionStatus
from app.ingestion.scheduler.manager import ingestion_manager
from app.ingestion.workers.async_worker import ingestion_worker

router = APIRouter(prefix="/ingestion", tags=["ingestion"])

@router.post("/start")
async def start_ingestion(config: IngestionConfig, background_tasks: BackgroundTasks):
    if ingestion_manager.state["status"] == "Running":
        raise HTTPException(status_code=400, detail="Ingestion is already running")
        
    targets = {
        "arxiv_papers": config.targets.arxiv_papers,
        "github_repos": config.targets.github_repos,
        "hf_models": config.targets.hf_models,
        "hf_datasets": config.targets.hf_datasets
    }
    
    ingestion_manager.start(targets)
    background_tasks.add_task(ingestion_worker.run_acquisition, targets)
    return {"message": "Bulk acquisition started", "targets": targets}

@router.post("/pause")
async def pause_ingestion():
    if ingestion_manager.state["status"] != "Running":
        raise HTTPException(status_code=400, detail="Ingestion is not running")
    ingestion_manager.pause()
    return {"message": "Bulk acquisition paused"}

@router.post("/resume")
async def resume_ingestion(background_tasks: BackgroundTasks):
    if ingestion_manager.state["status"] != "Paused":
        raise HTTPException(status_code=400, detail="Ingestion is not paused")
    
    ingestion_manager.resume()
    background_tasks.add_task(ingestion_worker.run_acquisition, ingestion_manager.targets)
    return {"message": "Bulk acquisition resumed"}

@router.post("/stop")
async def stop_ingestion():
    if ingestion_manager.state["status"] not in ["Running", "Paused"]:
        raise HTTPException(status_code=400, detail="Ingestion is not running or paused")
    ingestion_manager.stop()
    return {"message": "Bulk acquisition stopped"}

@router.get("/status", response_model=IngestionStatus)
async def get_status():
    state = ingestion_manager.get_status()
    return IngestionStatus(**state)

@router.get("/statistics")
async def get_statistics():
    state = ingestion_manager.get_status()
    return {
        "total_records": state["total_records"],
        "stats": state["stats"],
        "success_rate": state["success_rate"],
        "failed_requests": state["failed_requests"],
        "avg_speed": state["avg_speed"]
    }
