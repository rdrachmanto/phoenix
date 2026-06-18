from pathlib import Path
import json
import shutil

from phoenix.jobgraph import JobGraph
from phoenix.utils import now, atomic_write_json, log_event
from phoenix.config import STATE_ROOT


class BufferManager:
    def __init__(self, state_dir: Path):
        self.state_dir = Path(state_dir)
        self.checkpoint_dir = self.state_dir / "checkpoints"
        self.manifest_path = self.state_dir / "manifest.json"

        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        self.manifest = self.load_or_create_manifest()

    def empty_manifest(self):
        return {
            "run_id": "active",
            "created_at": now(),
            "completed": {},
        }

    def load_or_create_manifest(self):
        if not self.manifest_path.exists():
            manifest = self.empty_manifest()
            atomic_write_json(self.manifest_path, manifest)
            return manifest

        try:
            with open(self.manifest_path, "r") as f:
                manifest = json.load(f)
        except json.JSONDecodeError:
            broken_path = self.manifest_path.with_suffix(".broken.json")
            shutil.move(self.manifest_path, broken_path)

            log_event(
                "manifest_corrupt",
                broken_manifest=str(broken_path),
            )

            manifest = self.empty_manifest()
            atomic_write_json(self.manifest_path, manifest)

        manifest.setdefault("completed", {})
        return manifest

    def recover(self):
        completed = list(self.manifest["completed"].keys())

        log_event(
            "boot_recovery",
            completed=completed,
            completed_count=len(completed),
        )

        return completed

    def is_completed(self, job_id: str):
        return job_id in self.manifest["completed"]

    def completed_jobs(self):
        return set(self.manifest["completed"].keys())

    def write_checkpoint(self, job_id: str, metadata: dict):
        checkpoint_path = self.checkpoint_dir / f"{job_id}.json"

        payload = {
            "job_id": job_id,
            "written_at": now(),
            "metadata": metadata,
        }

        atomic_write_json(checkpoint_path, payload)
        return checkpoint_path

    def mark_completed(self, job_id: str, metadata: dict):
        checkpoint_path = self.write_checkpoint(job_id, metadata)

        self.manifest["completed"][job_id] = {
            "status": "done",
            "finished_at": now(),
            "checkpoint": str(checkpoint_path),
            "metadata_summary": {
                "duration_s": metadata.get("duration_s"),
                "energy_used_j": metadata.get("energy_used_j"),
                "useful_work": metadata.get("useful_work"),
            },
        }

        atomic_write_json(self.manifest_path, self.manifest)

        log_event(
            "checkpoint_saved",
            job_id=job_id,
            checkpoint=str(checkpoint_path),
        )

    def get_checkpoint_path(self, job_id: str):
        return self.manifest["completed"][job_id]["checkpoint"]

    def workflow_complete(self, graph: JobGraph):
        return all(self.is_completed(job_id) for job_id in graph.all_jobs())

    def archive_active_run(self):
        completed_root = STATE_ROOT / "completed"
        completed_root.mkdir(parents=True, exist_ok=True)

        run_name = f"run_{int(now())}"
        archive_path = completed_root / run_name

        shutil.move(str(self.state_dir), str(archive_path))

        log_event(
            "run_archived",
            archive=str(archive_path),
        )

        return archive_path

    def clear(self):
        if self.state_dir.exists():
            shutil.rmtree(self.state_dir)
