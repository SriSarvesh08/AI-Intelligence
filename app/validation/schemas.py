from pydantic import BaseModel
from typing import List, Dict, Any

class ValidationWarning(BaseModel):
    entity_id: str
    company_name: str
    issue_type: str # "Missing Field", "Low Confidence", "Invalid Data"
    description: str

class ValidationSummary(BaseModel):
    total_records: int
    valid_records: int
    invalid_records: int
    warnings: List[ValidationWarning]
    confidence_distribution: Dict[str, int] # e.g. {"High": 10, "Medium": 5, "Low": 2}
