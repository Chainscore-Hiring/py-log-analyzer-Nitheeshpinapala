import asyncio
import re
from datetime import datetime
from typing import Dict

class Worker:
    def __init__(self, port: int, worker_id: str, coordinator_url: str):
        self.worker_id = worker_id
        self.coordinator_url = coordinator_url
        self.port = port
    
    async def process_chunk(self, filepath: str, start: int, size: int) -> Dict:
        results = {"errors": 0, "total_requests": 0, "total_response_time": 0}
        with open(filepath, "r") as file:
            file.seek(start)
            chunk = file.read(size)
            lines = chunk.splitlines()
            
            for line in lines:
                match = re.match(
                    r"(?P<timestamp>\S+ \S+)\s(?P<level>\S+)\s(?P<message>.+?)(?:in (?P<response_time>\d+)ms)?",
                    line,
                )
                if match:
                    log_data = match.groupdict()
                    timestamp = datetime.strptime(log_data["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
                    level = log_data["level"]
                    if level == "ERROR":
                        results["errors"] += 1
                    elif level == "INFO" and log_data.get("response_time"):
                        results["total_requests"] += 1
                        results["total_response_time"] += int(log_data["response_time"])
        
        return results

    async def report_health(self) -> None:
        while True:
            print(f"Worker {self.worker_id} is alive.")
            await asyncio.sleep(10)

