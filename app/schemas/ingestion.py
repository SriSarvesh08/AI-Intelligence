from pydantic import BaseModel
from typing import Optional, Dict, List

class IngestionTarget(BaseModel):
    arxiv_papers: int = 1000
    github_repos: int = 1000
    hf_models: int = 1000
    hf_datasets: int = 500

class IngestionConfig(BaseModel):
    targets: IngestionTarget = IngestionTarget()

class IngestionStatus(BaseModel):
    status: str
    progress: float
    total_records: int
    current_source: Optional[str]
    current_page: int
    current_batch: int
    eta: Optional[str]
    stats: Dict[str, int]
    success_rate: float
    failed_requests: int
    avg_speed: float
    logs: List[str]
