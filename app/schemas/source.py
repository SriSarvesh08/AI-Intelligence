from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class SourceBase(BaseModel):
    name: str
    url: HttpUrl
    type: str

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    type: Optional[str] = None
    status: Optional[str] = None

class SourceResponse(SourceBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
