class Analyzer:
    def __init__(self):
        self.metrics = {"error_rate": 0, "avg_response_time": 0, "request_rate": 0}

    def update_metrics(self, new_data: Dict) -> None:
        total_requests = new_data.get("total_requests", 0)
        errors = new_data.get("errors", 0)
        total_response_time = new_data.get("total_response_time", 0)

        self.metrics["error_rate"] = errors / max(total_requests, 1)
        self.metrics["avg_response_time"] = total_response_time / max(total_requests, 1)

    def get_current_metrics(self) -> Dict:
        return self.metrics
