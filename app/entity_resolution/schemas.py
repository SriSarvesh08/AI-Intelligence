from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum

class PricingModel(str, Enum):
    FREE = "FREE"
    FREEMIUM = "FREEMIUM"
    PAID = "PAID"
    ENTERPRISE = "ENTERPRISE"

class SourceInfo(BaseModel):
    name: str
    url: str

class StartupContent(BaseModel):
    entityName: str
    data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
class StartupEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "STARTUP"
    source: SourceInfo
    content: StartupContent
    collectedAt: datetime = Field(default_factory=datetime.utcnow)

class ProductContent(BaseModel):
    startupName: str
    pricingModel: Optional[PricingModel] = None

class ProductEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "PRODUCT"
    source: SourceInfo
    content: ProductContent
    collectedAt: datetime = Field(default_factory=datetime.utcnow)

class ResearchPaperContent(BaseModel):
    title: str
    authors: List[str]
    paper_url: str
    github_url: Optional[str] = None
    github_stars: Optional[int] = None
    published_date: Optional[datetime] = None

class ResearchPaperEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "RESEARCH_PAPER"
    content: ResearchPaperContent

class JobContent(BaseModel):
    company: str
    date: Optional[datetime] = None
    is_remote: Optional[bool] = None
    role_family: Optional[str] = None

class JobEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "JOB"
    content: JobContent

# Legacy entity base used by other modules, kept for backward compatibility
class EntityBase(BaseModel):
    id: str
    company_name: Optional[str] = None
    website: Optional[str] = None
    founders: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    products: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    confidence_score: float = 1.0

class DuplicateCandidate(BaseModel):
    entity1_id: str
    entity2_id: str
    entity1: EntityBase
    entity2: EntityBase
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    match_reasons: List[str] = Field(default_factory=list)

class MergePreview(BaseModel):
    candidate: DuplicateCandidate
    merged_entity: EntityBase

class ResolutionStats(BaseModel):
    entities_before: int
    entities_after: int
    duplicates_removed: int
    average_confidence: float
