import httpx
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict

logger = logging.getLogger(__name__)

class JobsConnector:
    # Simulating 5 distinct AI Job boards
    SOURCES = [
        "https://wellfound.com/role/ai-engineer",
        "https://www.workatastartup.com/companies?query=AI",
        "https://www.linkedin.com/jobs/artificial-intelligence-jobs",
        "https://huggingface.co/jobs",
        "https://aijobs.net/"
    ]

    async def fetch_batch(self, page: int = 1, per_page: int = 10) -> List[Dict]:
        results = []
        now = datetime.utcnow()
        
        # Simulating Job extraction with 24-hr freshness constraint
        for source in self.SOURCES:
            for i in range(per_page):
                hours_ago = (page + i) % 24
                published_at = now - timedelta(hours=hours_ago)
                
                results.append({
                    "title": f"Senior AI Engineer - Role {i}",
                    "company": f"Canonical Startup {i}",
                    "url": f"{source}/job-{page}-{i}",
                    "published_at": published_at,
                    "is_remote": True,
                    "description": f"Full-text job description from {source}. Required skills: Python, PyTorch, LLMs.",
                    "source": "ai_jobs"
                })
                
        return results
