import asyncio
from typing import List, AsyncGenerator
from app.llm.chunker import TextChunker
from app.llm.client import GeminiClient
from app.llm.prompts import EXTRACTION_SYSTEM_PROMPT, build_extraction_prompt
from app.llm.validator import JSONValidator
from app.llm.schemas import ExtractedCompanyData

class ExtractorPipeline:
    def __init__(self, api_key: str = None):
        self.chunker = TextChunker()
        self.client = GeminiClient(api_key=api_key)
        self.validator = JSONValidator()

    async def extract_stream(self, text: str, source_url: str) -> AsyncGenerator[dict, None]:
        chunks = self.chunker.chunk_text(text)
        total_chunks = len(chunks)
        
        yield {
            "type": "init",
            "total_chunks": total_chunks,
            "message": f"Starting extraction for {source_url} ({total_chunks} chunks)"
        }

        extracted_results: List[ExtractedCompanyData] = []
        tokens_processed = 0
        
        for idx, chunk in enumerate(chunks):
            chunk_num = chunk["chunk_num"]
            chunk_text = chunk["text"]
            tokens = chunk["estimated_tokens"]
            
            yield {
                "type": "progress",
                "current_chunk": chunk_num,
                "message": f"Processing chunk {chunk_num}/{total_chunks}..."
            }
            
            prompt = build_extraction_prompt(chunk_text)
            
            # Simple retry loop for validation failures
            max_validation_retries = 1
            success = False
            
            for attempt in range(max_validation_retries + 1):
                try:
                    raw_response = await self.client.generate_content(EXTRACTION_SYSTEM_PROMPT, prompt)
                    tokens_processed += tokens
                    
                    validated_data, error = self.validator.validate(raw_response)
                    
                    if error:
                        yield {
                            "type": "log",
                            "message": f"Validation failed on chunk {chunk_num}: {error}. Retrying..."
                        }
                        if attempt == max_validation_retries:
                            yield {
                                "type": "log",
                                "message": f"Failed to extract valid JSON from chunk {chunk_num} after retries."
                            }
                        continue
                        
                    extracted_results.append(validated_data)
                    success = True
                    break
                    
                except Exception as e:
                    yield {
                        "type": "log",
                        "message": f"Error extracting chunk {chunk_num}: {str(e)}"
                    }
                    if attempt == max_validation_retries:
                        break
                    await asyncio.sleep(2)
                    
            if success:
                yield {
                    "type": "chunk_complete",
                    "chunk_num": chunk_num,
                    "tokens_processed": tokens_processed,
                    "message": f"Successfully extracted data from chunk {chunk_num}."
                }

        # Merge Phase
        yield {
            "type": "progress",
            "message": "Merging and deduplicating results..."
        }
        
        final_data = self._merge_results(extracted_results)
        
        yield {
            "type": "complete",
            "tokens_processed": tokens_processed,
            "final_data": final_data.model_dump() if final_data else None,
            "message": "Extraction complete."
        }

    def _merge_results(self, results: List[ExtractedCompanyData]) -> ExtractedCompanyData:
        if not results:
            return None
            
        # Basic merge logic: take the first non-null value for strings, union for lists
        merged = results[0].model_dump()
        
        for r in results[1:]:
            r_dict = r.model_dump()
            for key, value in r_dict.items():
                if isinstance(value, list):
                    # Union and deduplicate
                    merged[key] = list(set(merged[key] + value))
                elif isinstance(value, str) and value and not merged.get(key):
                    merged[key] = value
                elif key == "confidence_score":
                    # Average confidence
                    merged[key] = (merged[key] + value) / 2.0
                    
        return ExtractedCompanyData(**merged)
