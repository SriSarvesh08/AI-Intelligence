import httpx
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict

logger = logging.getLogger(__name__)

class NewsConnector:
    # Simulating 5 distinct AI news sources (e.g. TechCrunch AI, VentureBeat AI, etc.)
    SOURCES = [
        "https://techcrunch.com/category/artificial-intelligence/",
        "https://venturebeat.com/category/ai/",
        "https://www.wired.com/tag/artificial-intelligence/",
        "https://www.theverge.com/ai-artificial-intelligence",
        "https://www.technologyreview.com/topic/artificial-intelligence/"
    ]

    async def fetch_batch(self, page: int = 1, per_page: int = 10) -> List[Dict]:
        results = []
        now = datetime.utcnow()
        
        # Simulating High-Fidelity News extraction with 24-hr freshness
        for source in self.SOURCES:
            for i in range(per_page):
                # Generate a mock timestamp within the last 24 hours to prove relative date logic
                # Simulates parsing "X hours ago" -> exact ISO-8601
                hours_ago = (page * 2 + i) % 24 
                published_at = now - timedelta(hours=hours_ago)
                
                results.append({
                    "title": f"Breaking AI News {i} from {source}",
                    "url": f"{source}article-{page}-{i}",
                    "published_at": published_at,
                    "content": f"Full-text content extracted from {source}. This article discusses new AI models and was published {hours_ago} hours ago.",
                    "source": "ai_news"
                })
                
        return results
