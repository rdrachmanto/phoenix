import argparse
from pathlib import Path

import yaml

from phoenix.jobgraph import JobGraph
from phoenix.bufmanager import BufferManager
from phoenix.energy_manager import EnergyMonitor
from phoenix.scheduler import Scheduler
from phoenix.runner import JobRunner
from phoenix.utils import log_event
from phoenix.config import ACTIVE_STATE


def load_graph(path: Path):
    with open(path, "r") as f:
        return yaml.safe_load(f)["jobs"]


def main(args):
    if args.mode not in {"greedy", "predictor"}:
        raise ValueError("Mode must be either 'greedy' or 'predictor'")

    graph = JobGraph(load_graph(args.jobs))
    buffer = BufferManager(ACTIVE_STATE)
    energy = EnergyMonitor(available_joules=10.0)
    scheduler = Scheduler(graph, buffer, energy)
    runner = JobRunner(graph)

    recovered = buffer.recover()

    print(f"Recovered completed jobs: {recovered}")
    print(f"Scheduler mode: {args.mode}")

    log_event(
        "runtime_start",
        scheduler_mode=args.mode,
    )

    while not scheduler.done():
        if args.mode == "greedy":
            job_id = scheduler.greedy_pick()
        else:
            job_id = scheduler.predictor_guided_pick()

        if job_id is None:
            print("No job selected. Runtime is deferring.")
            log_event("runtime_defer")
            return

        print(f"Running job: {job_id}")

        metadata = runner.run(job_id)

        if graph.checkpoint_enabled(job_id):
            buffer.mark_completed(job_id, metadata)
        else:
            log_event(
                "checkpoint_skipped",
                job_id=job_id,
            )

    print("Workflow complete.")

    log_event(
        "workflow_complete",
        completed=list(buffer.completed_jobs()),
    )

    archive_path = buffer.archive_active_run()
    print(f"Archived completed run at: {archive_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", "-j", type=str)
    parser.add_argument("--mode", "-m", type=str)

    args = parser.parse_args()

    print(args)
    
    main(args)
