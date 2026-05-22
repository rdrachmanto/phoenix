from phoenix.utils import log_event

from phoenix.jobgraph import JobGraph
from phoenix.bufmanager import BufferManager
from phoenix.energy_manager import EnergyMonitor


class Scheduler:
    def __init__(self, graph: JobGraph, buffer: BufferManager, energy: EnergyMonitor):
        self.graph = graph
        self.buffer = buffer
        self.energy = energy

    def runnable_jobs(self):
        runnable = []

        for job_id in self.graph.all_jobs():
            if self.buffer.is_completed(job_id):
                continue

            deps = self.graph.deps(job_id)

            if all(self.buffer.is_completed(dep) for dep in deps):
                runnable.append(job_id)

        return runnable

    def greedy_pick(self):
        runnable = self.runnable_jobs()

        if not runnable:
            return None

        return runnable[0]

    def predictor_guided_pick(self):
        runnable = self.runnable_jobs()
        available = self.energy.available_energy()

        candidates = []

        for job_id in runnable:
            cost = self.graph.energy_cost(job_id)

            if cost <= available:
                candidates.append((cost, job_id))

        if not candidates:
            log_event(
                "defer",
                reason="no_runnable_job_fits_energy",
                available_energy_j=available,
                runnable=runnable,
            )
            return None

        candidates.sort(reverse=True)
        return candidates[0][1]

    def done(self):
        return self.buffer.workflow_complete(self.graph)
