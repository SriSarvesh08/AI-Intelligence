import asyncio
from app.database.database import AsyncSessionLocal
from app.ingestion.scheduler.manager import ingestion_manager
from app.ingestion.storage.repository import IngestionRepository
from app.ingestion.sources.arxiv import ArxivConnector
from app.ingestion.sources.github import GithubConnector
from app.ingestion.sources.huggingface import HuggingFaceConnector
from app.ingestion.sources.news import NewsConnector
from app.ingestion.sources.jobs import JobsConnector
from app.logger import log

class AsyncIngestionWorker:
    def __init__(self):
        self.repo = IngestionRepository()
        self.arxiv = ArxivConnector()
        self.github = GithubConnector()
        self.hf = HuggingFaceConnector()
        self.news = NewsConnector()
        self.jobs = JobsConnector()
        self.running_task = None

    async def ingest_arxiv(self, target: int):
        if target <= 0: return
        page = 0
        batch_size = min(100, target)
        processed = 0

        while processed < target and ingestion_manager.state["status"] == "Running":
            try:
                records = await self.arxiv.fetch_batch(start=page * batch_size, max_results=batch_size)
                if not records:
                    break
                    
                if processed + len(records) > target:
                    records = records[:target - processed]

                async with AsyncSessionLocal() as db:
                    await self.repo.insert_papers(db, records)

                processed += len(records)
                page += 1
                ingestion_manager.update_progress("arxiv_papers", len(records), page, page)
                
                await asyncio.sleep(1)
            except Exception as e:
                log.error(f"Error fetching arXiv: {e}")
                ingestion_manager.log(f"ArXiv Error: {e}")
                ingestion_manager.update_progress("arxiv_papers", 0, page, page, failed=1)
                await asyncio.sleep(3)

    async def ingest_github(self, target: int):
        if target <= 0: return
        page = 1
        batch_size = min(100, target)
        processed = 0

        while processed < target and ingestion_manager.state["status"] == "Running":
            try:
                records = await self.github.fetch_batch(page=page, per_page=batch_size)
                if not records:
                    break
                    
                if processed + len(records) > target:
                    records = records[:target - processed]

                async with AsyncSessionLocal() as db:
                    await self.repo.insert_repositories(db, records)

                processed += len(records)
                page += 1
                ingestion_manager.update_progress("github_repos", len(records), page, page)
                
                await asyncio.sleep(2)
            except Exception as e:
                log.error(f"Error fetching GitHub: {e}")
                ingestion_manager.log(f"GitHub Error: {e}")
                ingestion_manager.update_progress("github_repos", 0, page, page, failed=1)
                await asyncio.sleep(5)

    async def ingest_hf_models(self, target: int):
        if target <= 0: return
        page = 0
        batch_size = min(100, target)
        processed = 0

        while processed < target and ingestion_manager.state["status"] == "Running":
            try:
                records = await self.hf.fetch_models_batch(limit=batch_size, page=page)
                if not records:
                    break
                    
                if processed + len(records) > target:
                    records = records[:target - processed]

                async with AsyncSessionLocal() as db:
                    await self.repo.insert_models(db, records)

                processed += len(records)
                page += 1
                ingestion_manager.update_progress("hf_models", len(records), page, page)
                
                await asyncio.sleep(1)
            except Exception as e:
                log.error(f"Error fetching HF Models: {e}")
                ingestion_manager.log(f"HF Models Error: {e}")
                ingestion_manager.update_progress("hf_models", 0, page, page, failed=1)
                await asyncio.sleep(3)

    async def ingest_hf_datasets(self, target: int):
        if target <= 0: return
        page = 0
        batch_size = min(100, target)
        processed = 0

        while processed < target and ingestion_manager.state["status"] == "Running":
            try:
                records = await self.hf.fetch_datasets_batch(limit=batch_size, page=page)
                if not records:
                    break
                    
                if processed + len(records) > target:
                    records = records[:target - processed]

                async with AsyncSessionLocal() as db:
                    await self.repo.insert_datasets(db, records)

                processed += len(records)
                page += 1
                ingestion_manager.update_progress("hf_datasets", len(records), page, page)
                
                await asyncio.sleep(1)
            except Exception as e:
                log.error(f"Error fetching HF Datasets: {e}")
                ingestion_manager.log(f"HF Datasets Error: {e}")
                ingestion_manager.update_progress("hf_datasets", 0, page, page, failed=1)
                await asyncio.sleep(3)

    async def ingest_news(self, target: int):
        if target <= 0: return
        page = 1
        batch_size = min(10, target)
        processed = 0

        while processed < target and ingestion_manager.state["status"] == "Running":
            try:
                records = await self.news.fetch_batch(page=page, per_page=batch_size)
                if not records: break
                
                if processed + len(records) > target:
                    records = records[:target - processed]

                # News records are processed in memory for Phase II demonstration
                processed += len(records)
                page += 1
                ingestion_manager.update_progress("news", len(records), page, page)
                await asyncio.sleep(1)
            except Exception as e:
                log.error(f"Error fetching News: {e}")
                ingestion_manager.log(f"News Error: {e}")
                ingestion_manager.update_progress("news", 0, page, page, failed=1)
                break

    async def ingest_jobs(self, target: int):
        if target <= 0: return
        page = 1
        batch_size = min(10, target)
        processed = 0

        while processed < target and ingestion_manager.state["status"] == "Running":
            try:
                records = await self.jobs.fetch_batch(page=page, per_page=batch_size)
                if not records: break
                
                if processed + len(records) > target:
                    records = records[:target - processed]

                # Job records are processed in memory for Phase II demonstration
                processed += len(records)
                page += 1
                ingestion_manager.update_progress("jobs", len(records), page, page)
                await asyncio.sleep(1)
            except Exception as e:
                log.error(f"Error fetching Jobs: {e}")
                ingestion_manager.log(f"Jobs Error: {e}")
                ingestion_manager.update_progress("jobs", 0, page, page, failed=1)
                break

    async def run_acquisition(self, targets: dict):
        try:
            tasks = []
            if targets.get("arxiv_papers", 0) > 0:
                tasks.append(self.ingest_arxiv(targets["arxiv_papers"]))
            if targets.get("github_repos", 0) > 0:
                tasks.append(self.ingest_github(targets["github_repos"]))
            if targets.get("hf_models", 0) > 0:
                tasks.append(self.ingest_hf_models(targets["hf_models"]))
            if targets.get("hf_datasets", 0) > 0:
                tasks.append(self.ingest_hf_datasets(targets["hf_datasets"]))
            if targets.get("news", 0) > 0:
                tasks.append(self.ingest_news(targets["news"]))
            if targets.get("jobs", 0) > 0:
                tasks.append(self.ingest_jobs(targets["jobs"]))

            await asyncio.gather(*tasks)
            
            if ingestion_manager.state["status"] == "Running":
                ingestion_manager.state["status"] = "Completed"
                ingestion_manager.log("Bulk acquisition completed successfully.")
        except Exception as e:
            log.error(f"Acquisition runner failed: {e}")
            ingestion_manager.state["status"] = "Stopped"
            ingestion_manager.log(f"Critical error: {e}")

ingestion_worker = AsyncIngestionWorker()
