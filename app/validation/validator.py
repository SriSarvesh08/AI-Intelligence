from typing import List, Tuple
import re
from app.entity_resolution.schemas import EntityBase
from app.validation.schemas import ValidationWarning, ValidationSummary

class DataValidator:
    def __init__(self, confidence_threshold: float = 0.70):
        self.confidence_threshold = confidence_threshold

    def validate_entities(self, entities: List[EntityBase]) -> Tuple[List[EntityBase], ValidationSummary]:
        valid_records = 0
        invalid_records = 0
        warnings = []
        confidence_dist = {"High (>0.9)": 0, "Medium (0.7-0.9)": 0, "Low (<0.7)": 0}

        for entity in entities:
            is_valid = True
            
            # 1. Confidence Threshold Check
            if entity.confidence_score < self.confidence_threshold:
                is_valid = False
                warnings.append(ValidationWarning(
                    entity_id=entity.id,
                    company_name=entity.company_name or "Unknown",
                    issue_type="Low Confidence",
                    description=f"Confidence score {entity.confidence_score:.2f} is below threshold {self.confidence_threshold}"
                ))

            # 2. Missing Field Detection
            if not entity.company_name:
                is_valid = False
                warnings.append(ValidationWarning(
                    entity_id=entity.id,
                    company_name="Unknown",
                    issue_type="Missing Field",
                    description="Company name is missing"
                ))
                
            if not entity.website:
                warnings.append(ValidationWarning(
                    entity_id=entity.id,
                    company_name=entity.company_name or "Unknown",
                    issue_type="Missing Field",
                    description="Website is missing (Warning only)"
                ))

            # 3. Invalid Data Detection (Basic URL format check if present)
            if entity.website and not re.match(r'^(http|https)://|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', entity.website):
                warnings.append(ValidationWarning(
                    entity_id=entity.id,
                    company_name=entity.company_name or "Unknown",
                    issue_type="Invalid Data",
                    description=f"Website URL format appears invalid: {entity.website}"
                ))

            # Update Metrics
            if is_valid:
                valid_records += 1
            else:
                invalid_records += 1

            if entity.confidence_score >= 0.9:
                confidence_dist["High (>0.9)"] += 1
            elif entity.confidence_score >= 0.7:
                confidence_dist["Medium (0.7-0.9)"] += 1
            else:
                confidence_dist["Low (<0.7)"] += 1

        summary = ValidationSummary(
            total_records=len(entities),
            valid_records=valid_records,
            invalid_records=invalid_records,
            warnings=warnings,
            confidence_distribution=confidence_dist
        )

        return entities, summary
