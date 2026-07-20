from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.database.models import Source
from app.schemas.source import SourceCreate, SourceUpdate

async def get_sources(db: AsyncSession):
    result = await db.execute(select(Source))
    return result.scalars().all()

async def get_source_by_id(db: AsyncSession, source_id: str):
    result = await db.execute(select(Source).where(Source.id == source_id))
    return result.scalars().first()

async def create_source(db: AsyncSession, source: SourceCreate):
    db_source = Source(
        name=source.name,
        url=str(source.url),
        type=source.type
    )
    try:
        db.add(db_source)
        await db.commit()
        await db.refresh(db_source)
        return db_source
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Source with this URL already exists")

async def update_source(db: AsyncSession, source_id: str, source: SourceUpdate):
    db_source = await get_source_by_id(db, source_id)
    if not db_source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    
    update_data = source.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "url" and value is not None:
            setattr(db_source, key, str(value))
        else:
            setattr(db_source, key, value)
            
    try:
        await db.commit()
        await db.refresh(db_source)
        return db_source
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Another source with this URL already exists")

async def delete_source(db: AsyncSession, source_id: str):
    db_source = await get_source_by_id(db, source_id)
    if not db_source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    
    await db.delete(db_source)
    await db.commit()
    return {"message": "Source deleted successfully"}
