import httpx
from typing import List, Dict

class HuggingFaceConnector:
    BASE_MODELS_URL = "https://huggingface.co/api/models"
    BASE_DATASETS_URL = "https://huggingface.co/api/datasets"

    async def fetch_models_batch(self, limit: int = 100, page: int = 0) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            # We use limit and an offset calculated by limit*page 
            # Note: The HF API usually doesn't have offset, but limit/sort works. We can just use search logic or list.
            params = {
                "limit": limit,
                "sort": "downloads",
                "direction": "-1",
                "full": "true" # to get all metadata
            }
            # simple pagination hack for HF API list endpoints: pass search terms or just accept what we get for phase 1
            # Real HF API doesn't support easy offset pagination for the raw list beyond basic limit. 
            response = await client.get(self.BASE_MODELS_URL, params=params, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data:
                results.append({
                    "name": item.get("id", ""),
                    "author": item.get("author", ""),
                    "downloads": item.get("downloads", 0),
                    "likes": item.get("likes", 0),
                    "pipeline_tag": item.get("pipeline_tag", ""),
                    "library": item.get("library_name", ""),
                    "license": "", # License requires deeper parsing from siblings in HF
                    "url": f"https://huggingface.co/{item.get('id', '')}",
                    "source": "huggingface_models"
                })
            return results

    async def fetch_datasets_batch(self, limit: int = 100, page: int = 0) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            params = {
                "limit": limit,
                "sort": "downloads",
                "direction": "-1",
                "full": "true"
            }
            response = await client.get(self.BASE_DATASETS_URL, params=params, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data:
                # HF dataset tags
                tags = item.get("tags", [])
                task_cats = [t.replace("task_categories:", "") for t in tags if t.startswith("task_categories:")]
                langs = [t.replace("language:", "") for t in tags if t.startswith("language:")]
                
                results.append({
                    "name": item.get("id", ""),
                    "author": item.get("author", ""),
                    "downloads": item.get("downloads", 0),
                    "likes": item.get("likes", 0),
                    "task_categories": ", ".join(task_cats),
                    "languages": ", ".join(langs),
                    "license": "",
                    "url": f"https://huggingface.co/datasets/{item.get('id', '')}",
                    "source": "huggingface_datasets"
                })
            return results
