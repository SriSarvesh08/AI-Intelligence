import json
import csv
import io
from typing import List
from app.entity_resolution.schemas import EntityBase
from app.validation.schemas import ValidationSummary

class DataExporter:
    
    @staticmethod
    def export_to_json(entities: List[EntityBase]) -> str:
        # Convert Pydantic models to dicts
        data = [e.model_dump() for e in entities]
        return json.dumps(data, indent=2)

    @staticmethod
    def export_to_csv(entities: List[EntityBase]) -> str:
        if not entities:
            return ""
            
        output = io.StringIO()
        # Define base scalar fields
        fieldnames = ["id", "company_name", "website", "location", "industry", "description", "confidence_score"]
        # Define list fields to flatten
        list_fields = ["founders", "products", "technologies", "keywords"]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames + list_fields)
        writer.writeheader()
        
        for entity in entities:
            row = entity.model_dump(include=set(fieldnames))
            
            # Flatten lists by joining with semicolons
            for field in list_fields:
                val = getattr(entity, field)
                row[field] = "; ".join(val) if val else ""
                
            writer.writerow(row)
            
        return output.getvalue()

    @staticmethod
    def export_report(summary: ValidationSummary) -> str:
        output = io.StringIO()
        output.write("DATA VALIDATION REPORT\n")
        output.write("======================\n\n")
        
        output.write(f"Total Records: {summary.total_records}\n")
        output.write(f"Valid Records: {summary.valid_records}\n")
        output.write(f"Invalid Records: {summary.invalid_records}\n\n")
        
        output.write("Confidence Distribution:\n")
        for k, v in summary.confidence_distribution.items():
            output.write(f"- {k}: {v}\n")
            
        output.write("\nWarnings and Errors:\n")
        output.write("--------------------\n")
        if not summary.warnings:
            output.write("No warnings found.\n")
        else:
            for w in summary.warnings:
                output.write(f"[{w.issue_type}] {w.company_name} (ID: {w.entity_id}): {w.description}\n")
                
        return output.getvalue()
