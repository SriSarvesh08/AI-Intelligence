from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.database import get_db
from app.schemas.source import SourceCreate, SourceUpdate, SourceResponse
from app.database import repository

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.post("/", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(source: SourceCreate, db: AsyncSession = Depends(get_db)):
    return await repository.create_source(db, source)

@router.get("/", response_model=List[SourceResponse])
async def get_sources(db: AsyncSession = Depends(get_db)):
    return await repository.get_sources(db)

@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(source_id: str, db: AsyncSession = Depends(get_db)):
    source = await repository.get_source_by_id(db, source_id)
    if not source:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return source

@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(source_id: str, source: SourceUpdate, db: AsyncSession = Depends(get_db)):
    return await repository.update_source(db, source_id, source)

@router.delete("/{source_id}", status_code=status.HTTP_200_OK)
async def delete_source(source_id: str, db: AsyncSession = Depends(get_db)):
    return await repository.delete_source(db, source_id)
