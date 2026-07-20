from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.database.models import CrawlJob
from app.schemas.crawl_job import CrawlJobCreate
from datetime import datetime

async def get_jobs(db: AsyncSession):
    result = await db.execute(select(CrawlJob).order_by(CrawlJob.created_at.desc()))
    return result.scalars().all()

async def get_job_by_id(db: AsyncSession, job_id: str):
    result = await db.execute(select(CrawlJob).where(CrawlJob.id == job_id))
    return result.scalars().first()

async def create_job(db: AsyncSession, job: CrawlJobCreate):
    db_job = CrawlJob(
        source_id=job.source_id,
        priority=job.priority
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

async def cancel_job(db: AsyncSession, job_id: str):
    db_job = await get_job_by_id(db, job_id)
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    if db_job.status in ["Completed", "Failed"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot cancel a job in {db_job.status} state")

    db_job.status = "Failed"
    db_job.logs = "Job cancelled by user"
    db_job.finished_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_job)
    return db_job

async def retry_job(db: AsyncSession, job_id: str):
    db_job = await get_job_by_id(db, job_id)
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db_job.status = "Queued"
    db_job.current_stage = "Queued"
    db_job.progress = 0
    db_job.pages_processed = 0
    db_job.started_at = None
    db_job.finished_at = None
    db_job.logs = None
    await db.commit()
    await db.refresh(db_job)
    return db_job
