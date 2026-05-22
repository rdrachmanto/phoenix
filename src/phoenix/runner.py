import shlex
import subprocess
import yaml
from pathlib import Path

from phoenix.jobgraph import JobGraph
from phoenix.utils import now


class JobRunner:
    def __init__(self, graph: JobGraph) -> None:
        self.graph = graph

    def run(self, job_id: str):
        spec = self.graph.get(job_id)

        # log start here

        start = now()

        result = subprocess.run(
            spec["command"],
            shell=True,
            capture_output=True,
            text=True
        )

        finish = now()

        duration = finish - start

        # log end here

        return {
            "started_at": start,
            "finished_at": finish,
            "duration_s": duration,
            "useful_work": self.graph.useful_work(job_id),
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

