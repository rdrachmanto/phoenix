import shlex
import subprocess
import yaml
from pathlib import Path


def read_jobq(path: Path):
    with open(path, "r") as f:
        return yaml.safe_load(f)["jobs"]


def get_runnable_jobs():
    pass


def load_manifest():
    pass


def write_manifest():
    pass


def save_checkpoint():
    pass


def run_job(jobd):
    for ji, jv in jobd.items():
        jo = subprocess.run(jv["command"], capture_output=True, text=True, shell=True)
        print(jo)
