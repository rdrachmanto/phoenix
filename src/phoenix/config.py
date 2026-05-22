from pathlib import Path


STATE_ROOT = Path("runtime_state")
ACTIVE_STATE = STATE_ROOT / "active"
CHECKPOINT_DIR = ACTIVE_STATE / "checkpoints"
MANIFEST_PATH = ACTIVE_STATE / "manifest.json"

LOG_DIR = Path("logs")
EVENT_LOG = LOG_DIR / "events.jsonl"
