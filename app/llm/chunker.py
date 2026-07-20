from typing import List, Dict

class TextChunker:
    def __init__(self, chunk_size: int = 15000, overlap: int = 1000):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def estimate_tokens(self, text: str) -> int:
        # A simple approximation: ~4 characters per token for English text
        return len(text) // 4

    def chunk_text(self, text: str) -> List[Dict[str, any]]:
        chunks = []
        text_length = len(text)
        
        # Calculate characters based on token approximation
        chars_per_chunk = self.chunk_size * 4
        chars_overlap = self.overlap * 4
        
        if text_length <= chars_per_chunk:
            return [{
                "chunk_num": 1,
                "text": text,
                "estimated_tokens": self.estimate_tokens(text)
            }]

        start = 0
        chunk_num = 1
        
        while start < text_length:
            end = min(start + chars_per_chunk, text_length)
            
            # If we're not at the end of the text, try to find a natural break (newline or space)
            if end < text_length:
                # Look backwards for a newline within the last 500 characters
                break_point = text.rfind('\n', max(start, end - 500), end)
                if break_point != -1:
                    end = break_point + 1
                else:
                    # Fallback to space
                    break_point = text.rfind(' ', max(start, end - 100), end)
                    if break_point != -1:
                        end = break_point + 1
            
            chunk_text = text[start:end]
            chunks.append({
                "chunk_num": chunk_num,
                "text": chunk_text,
                "estimated_tokens": self.estimate_tokens(chunk_text)
            })
            
            chunk_num += 1
            start = end - chars_overlap
            
            # Prevent infinite loops if overlap is somehow larger than progression
            if start <= end - chars_per_chunk + chars_overlap:
                start = end - chars_overlap

        return chunks
