class Coordinator:
    def __init__(self, port: int):
        self.port = port
        self.workers = {}
        self.results = {"errors": 0, "total_requests": 0, "total_response_time": 0}

    async def distribute_work(self, filepath: str) -> None:
        chunk_size = 1024 * 1024  # 1 MB
        file_size = os.path.getsize(filepath)
        chunks = [(i, min(chunk_size, file_size - i)) for i in range(0, file_size, chunk_size)]

        for worker_id, (start, size) in zip(self.workers.keys(), chunks):
            worker = self.workers[worker_id]
            results = await worker.process_chunk(filepath, start, size)
            self.receive_results(worker_id, results)

    async def handle_worker_failure(self, worker_id: str) -> None:
        print(f"Worker {worker_id} has failed. Reassigning work.")
        # Logic to redistribute work

    def receive_results(self, worker_id: str, results: Dict) -> None:
        self.results["errors"] += results["errors"]
        self.results["total_requests"] += results["total_requests"]
        self.results["total_response_time"] += results["total_response_time"]

    def get_aggregated_results(self) -> Dict:
        return self.results

