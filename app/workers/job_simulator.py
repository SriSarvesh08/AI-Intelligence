import asyncio
from datetime import datetime
from app.database.database import AsyncSessionLocal
from app.database.job_repository import get_job_by_id

async def simulate_crawl_job(job_id: str):
    stages = [
        {"name": "Collecting URLs", "progress": 25, "time": 3},
        {"name": "Downloading", "progress": 60, "time": 5},
        {"name": "Extracting", "progress": 90, "time": 4},
        {"name": "Completed", "progress": 100, "time": 1}
    ]

    # Start the job
    async with AsyncSessionLocal() as db:
        job = await get_job_by_id(db, job_id)
        if not job or job.status == "Failed":
            return
        
        job.status = "Running"
        job.started_at = datetime.utcnow()
        await db.commit()

    # Process through stages
    for stage in stages:
        await asyncio.sleep(stage["time"])
        
        async with AsyncSessionLocal() as db:
            job = await get_job_by_id(db, job_id)
            
            # Check if job was cancelled
            if not job or job.status == "Failed":
                return
            
            job.current_stage = stage["name"]
            job.progress = stage["progress"]
            
            if stage["name"] == "Downloading" or stage["name"] == "Extracting":
                job.pages_processed += 15

            if stage["name"] == "Completed":
                job.status = "Completed"
                job.finished_at = datetime.utcnow()
                job.logs = "Job finished successfully."
                
            await db.commit()
