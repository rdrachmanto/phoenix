import time
import json
from pathlib import Path
import os

from phoenix.config import ACTIVE_STATE, CHECKPOINT_DIR, LOG_DIR, EVENT_LOG

def now():
    return time.time()


def ensure_dirs():
    ACTIVE_STATE.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def atomic_write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = path.with_suffix(path.suffix + ".tmp")

    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)
        f.flush()
        os.fsync(f.fileno())

    os.replace(tmp_path, path)


def log_event(event_type: str, **fields):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    event = {
        "time": now(),
        "event": event_type,
        **fields,
    }

    with open(EVENT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")
