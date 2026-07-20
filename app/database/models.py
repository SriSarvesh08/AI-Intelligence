import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from app.database.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    url = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class CrawlJob(Base):
    __tablename__ = "crawl_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=False)
    status = Column(String, default="Queued", nullable=False)
    priority = Column(String, default="Medium", nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    pages_processed = Column(Integer, default=0, nullable=False)
    current_stage = Column(String, default="Queued", nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    logs = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Paper(Base):
    __tablename__ = "papers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    authors = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    categories = Column(String, nullable=False)
    published_date = Column(DateTime, nullable=True)
    pdf_url = Column(String, nullable=True)
    source = Column(String, default="arxiv", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    language = Column(String, nullable=True)
    license = Column(String, nullable=True)
    topics = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    url = Column(String, nullable=False)
    updated_date = Column(DateTime, nullable=True)
    source = Column(String, default="github", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Model(Base):
    __tablename__ = "models"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    author = Column(String, nullable=True)
    downloads = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    pipeline_tag = Column(String, nullable=True)
    library = Column(String, nullable=True)
    license = Column(String, nullable=True)
    url = Column(String, nullable=False)
    source = Column(String, default="huggingface_models", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    author = Column(String, nullable=True)
    downloads = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    task_categories = Column(String, nullable=True)
    languages = Column(String, nullable=True)
    license = Column(String, nullable=True)
    url = Column(String, nullable=False)
    source = Column(String, default="huggingface_datasets", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
