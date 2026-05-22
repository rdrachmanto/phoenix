class JobGraph:
    def __init__(self, jobs: dict) -> None:
        self.jobs = jobs

    def all_jobs(self):
        return list(self.jobs.keys())

    def get(self, job_id):
        return self.jobs[job_id]

    def deps(self, job_id):
        return self.jobs[job_id].get("deps", [])

    def energy_cost(self, job_id):
        return float(self.jobs[job_id].get("energy_cost", 1.0))

    def useful_work(self, job_id):
        return float(self.jobs[job_id].get("useful_work", 1.0))

    def checkpoint_enabled(self, job_id):
        return bool(self.jobs[job_id].get("checkpoint", True))
