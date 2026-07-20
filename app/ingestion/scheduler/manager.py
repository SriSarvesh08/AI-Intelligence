from typing import Dict, Any, List
from datetime import datetime
import time

class IngestionManager:
    def __init__(self):
        self.state = {
            "status": "Idle", # Idle, Running, Paused, Stopped, Completed
            "progress": 0.0,
            "total_records": 0,
            "current_source": None,
            "current_page": 1,
            "current_batch": 0,
            "eta": None,
            "stats": {
                "arxiv": 0,
                "github": 0,
                "hf_models": 0,
                "hf_datasets": 0,
                "news": 0,
                "jobs": 0
            },
            "success_rate": 100.0,
            "failed_requests": 0,
            "avg_speed": 0.0,
            "logs": []
        }
        self.start_time = None
        self.targets = {}
        self.total_target = 0

    def start(self, targets: dict):
        self.targets = targets
        self.total_target = sum(targets.values())
        self.state["status"] = "Running"
        self.state["progress"] = 0.0
        self.state["total_records"] = 0
        self.state["stats"] = {k: 0 for k in targets.keys()}
        self.state["failed_requests"] = 0
        self.state["logs"] = []
        self.start_time = time.time()
        self.log("Started bulk acquisition.")

    def pause(self):
        self.state["status"] = "Paused"
        self.log("Paused bulk acquisition.")

    def resume(self):
        self.state["status"] = "Running"
        self.log("Resumed bulk acquisition.")

    def stop(self):
        self.state["status"] = "Stopped"
        self.log("Stopped bulk acquisition.")

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.state["logs"].append(f"[{timestamp}] {message}")
        if len(self.state["logs"]) > 100:
            self.state["logs"].pop(0)

    def update_progress(self, source: str, count: int, page: int, batch: int, failed: int = 0):
        self.state["stats"][source] += count
        self.state["total_records"] += count
        self.state["failed_requests"] += failed
        self.state["current_source"] = source
        self.state["current_page"] = page
        self.state["current_batch"] = batch

        if self.total_target > 0:
            self.state["progress"] = min(100.0, (self.state["total_records"] / self.total_target) * 100.0)

        total_requests = self.state["total_records"] + self.state["failed_requests"]
        if total_requests > 0:
            self.state["success_rate"] = (self.state["total_records"] / total_requests) * 100.0

        if self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                self.state["avg_speed"] = self.state["total_records"] / elapsed
                if self.state["avg_speed"] > 0:
                    remaining = (self.total_target - self.state["total_records"]) / self.state["avg_speed"]
                    self.state["eta"] = f"{int(remaining)}s"

    def get_status(self) -> Dict[str, Any]:
        return self.state

ingestion_manager = IngestionManager()
