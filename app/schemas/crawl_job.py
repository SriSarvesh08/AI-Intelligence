from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CrawlJobBase(BaseModel):
    source_id: str
    priority: str
    max_pages: Optional[int] = None # Added for frontend compatibility

class CrawlJobCreate(CrawlJobBase):
    pass

class CrawlJobResponse(CrawlJobBase):
    id: str
    status: str
    progress: int
    pages_processed: int
    current_stage: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    logs: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
