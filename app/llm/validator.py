import json
from pydantic import ValidationError
from typing import Tuple, Optional
from app.llm.schemas import ExtractedCompanyData

class JSONValidator:
    @staticmethod
    def clean_json_string(text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
            
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()

    @staticmethod
    def validate(json_str: str) -> Tuple[Optional[ExtractedCompanyData], Optional[str]]:
        try:
            cleaned_str = JSONValidator.clean_json_string(json_str)
            data_dict = json.loads(cleaned_str)
            validated_data = ExtractedCompanyData(**data_dict)
            return validated_data, None
        except json.JSONDecodeError as e:
            return None, f"Failed to parse JSON: {str(e)}"
        except ValidationError as e:
            return None, f"JSON failed schema validation: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error during validation: {str(e)}"
