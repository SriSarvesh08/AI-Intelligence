from typing import List, Optional
from pydantic import BaseModel, Field

class ExtractedCompanyData(BaseModel):
    company_name: Optional[str] = Field(None, description="The name of the company")
    description: Optional[str] = Field(None, description="A brief description of what the company does")
    industry: Optional[str] = Field(None, description="The industry the company operates in")
    location: Optional[str] = Field(None, description="Headquarters or primary location")
    website: Optional[str] = Field(None, description="The official website URL")
    founders: List[str] = Field(default_factory=list, description="List of founders")
    employees: Optional[str] = Field(None, description="Number of employees or company size")
    funding: Optional[str] = Field(None, description="Total funding amount or recent rounds")
    products: List[str] = Field(default_factory=list, description="List of primary products or services")
    technologies: List[str] = Field(default_factory=list, description="Technologies, frameworks, or tools used")
    keywords: List[str] = Field(default_factory=list, description="Key terms associated with the company")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in the extracted data from 0.0 to 1.0")
    missing_fields: List[str] = Field(default_factory=list, description="List of fields that could not be extracted from the text")

class ExtractionJobRequest(BaseModel):
    text: str = Field(..., description="The cleaned webpage text to extract data from")
    source_url: str = Field(..., description="The URL the text was scraped from")
