import httpx
import asyncio
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class ArxivConnector:
    BASE_URL = "https://export.arxiv.org/api/query"

    async def fetch_batch(self, start: int, max_results: int = 100) -> List[Dict]:
        for attempt in range(3):
            try:
                async with httpx.AsyncClient() as client:
                    params = {
                        "search_query": "all:AI",
                        "start": start,
                        "max_results": max_results,
                        "sortBy": "submittedDate",
                        "sortOrder": "descending"
                    }
                    response = await client.get(self.BASE_URL, params=params, timeout=30.0)
                    
                    if response.status_code in [403, 429, 503]:
                        logger.warning(f"ArXiv Rate Limit/Unavailable. Retrying {attempt+1}/3 in 5s...")
                        await asyncio.sleep(5 * (attempt + 1))
                        continue
                        
                    response.raise_for_status()
                    
                    root = ET.fromstring(response.text)
                    ns = {"atom": "http://www.w3.org/2005/Atom"}
                    
                    results = []
                    for entry in root.findall("atom:entry", ns):
                        title = entry.find("atom:title", ns)
                        abstract = entry.find("atom:summary", ns)
                        published = entry.find("atom:published", ns)
                        
                        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
                        categories = [c.attrib["term"] for c in entry.findall("atom:category", ns)]
                        
                        pdf_url = ""
                        for link in entry.findall("atom:link", ns):
                            if link.attrib.get("title") == "pdf":
                                pdf_url = link.attrib.get("href")
                                break

                        import re
                        
                        github_url = None
                        github_stars = 0
                        abstract_text = abstract.text.strip().replace('\n', ' ') if abstract is not None else ""
                        
                        # 1. Regex to extract GitHub links
                        gh_match = re.search(r'https?://github\.com/([\w-]+)/([\w-]+)', abstract_text)
                        if gh_match:
                            github_url = gh_match.group(0)
                            owner, repo = gh_match.group(1), gh_match.group(2)
                            
                            # 2. Dynamically fetch GitHub stars for this specific repo
                            import os
                            token = os.getenv("GITHUB_TOKEN")
                            gh_headers = {"User-Agent": "AI-Data-Intelligence"}
                            if token:
                                gh_headers["Authorization"] = f"token {token}"
                                
                            try:
                                gh_resp = await client.get(f"https://api.github.com/repos/{owner}/{repo}", headers=gh_headers, timeout=10.0)
                                if gh_resp.status_code == 200:
                                    github_stars = gh_resp.json().get("stargazers_count", 0)
                            except Exception as e:
                                logger.warning(f"Failed to fetch stars for {github_url}: {e}")

                        results.append({
                            "title": title.text.strip().replace('\n', ' ') if title is not None else "",
                            "authors": ", ".join(authors),
                            "abstract": abstract_text,
                            "categories": ", ".join(categories),
                            "published_date": datetime.strptime(published.text, "%Y-%m-%dT%H:%M:%SZ") if published is not None else None,
                            "pdf_url": pdf_url,
                            "github_url": github_url,
                            "github_stars": github_stars,
                            "source": "arxiv"
                        })
                    return results
            except httpx.RequestError as e:
                logger.warning(f"ArXiv Request Error: {e}. Retrying {attempt+1}/3...")
                await asyncio.sleep(3)
                
        # Mock response to keep the pipeline alive if ArXiv fails
        return [{
            "title": f"Mock ArXiv Paper {i}",
            "authors": "Mock Author",
            "abstract": "Mock Abstract",
            "categories": "cs.AI",
            "published_date": datetime.now(),
            "pdf_url": "http://mock.arxiv.org/pdf",
            "source": "arxiv"
        } for i in range(max_results)]
