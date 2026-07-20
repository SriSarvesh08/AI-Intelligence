from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.database.models import Paper, Repository, Model, Dataset
from app.logger import log

class IngestionRepository:
    async def insert_papers(self, db: AsyncSession, papers: List[dict]):
        if not papers: return
        db_papers = [Paper(**p) for p in papers]
        db.add_all(db_papers)
        await db.commit()

    async def insert_repositories(self, db: AsyncSession, repos: List[dict]):
        if not repos: return
        db_repos = [Repository(**r) for r in repos]
        db.add_all(db_repos)
        await db.commit()

    async def insert_models(self, db: AsyncSession, models: List[dict]):
        if not models: return
        db_models = [Model(**m) for m in models]
        db.add_all(db_models)
        await db.commit()

    async def insert_datasets(self, db: AsyncSession, datasets: List[dict]):
        if not datasets: return
        db_datasets = [Dataset(**d) for d in datasets]
        db.add_all(db_datasets)
        await db.commit()
