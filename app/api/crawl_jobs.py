from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.database import get_db
from app.schemas.crawl_job import CrawlJobCreate, CrawlJobResponse
from app.database import job_repository
from app.workers.job_simulator import simulate_crawl_job

router = APIRouter(prefix="/crawl-jobs", tags=["Crawl Jobs"])

@router.post("/", response_model=CrawlJobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job: CrawlJobCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    db_job = await job_repository.create_job(db, job)
    background_tasks.add_task(simulate_crawl_job, db_job.id)
    return db_job

@router.get("/", response_model=List[CrawlJobResponse])
async def get_jobs(db: AsyncSession = Depends(get_db)):
    return await job_repository.get_jobs(db)

@router.get("/{job_id}", response_model=CrawlJobResponse)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    job = await job_repository.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.put("/{job_id}/cancel", response_model=CrawlJobResponse)
async def cancel_job(job_id: str, db: AsyncSession = Depends(get_db)):
    return await job_repository.cancel_job(db, job_id)

@router.put("/{job_id}/retry", response_model=CrawlJobResponse)
async def retry_job(job_id: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    db_job = await job_repository.retry_job(db, job_id)
    background_tasks.add_task(simulate_crawl_job, db_job.id)
    return db_job
