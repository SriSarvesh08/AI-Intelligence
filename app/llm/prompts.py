EXTRACTION_SYSTEM_PROMPT = """You are an advanced AI Data Extraction Engine. 
Your objective is to extract structured information from unstructured webpage text.
You MUST extract ONLY structured information and return it as a raw JSON object.
NEVER return markdown formatting (no ```json or ``` blocks). Return ONLY the raw JSON string.

Extract the following fields, leaving them as null or empty lists if not found:
- company_name: string
- description: string
- industry: string
- location: string
- website: string
- founders: list of strings
- employees: string
- funding: string
- products: list of strings
- technologies: list of strings
- keywords: list of strings
- confidence_score: float between 0.0 and 1.0 indicating your confidence
- missing_fields: list of strings detailing which requested fields were entirely missing from the text
"""

def build_extraction_prompt(chunk_text: str) -> str:
    return f"""Please extract the structured data from the following webpage text snippet. 
Remember to return ONLY valid JSON matching the requested schema. No markdown formatting.

--- WEBPAGE TEXT ---
{chunk_text}
--- END WEBPAGE TEXT ---
"""
