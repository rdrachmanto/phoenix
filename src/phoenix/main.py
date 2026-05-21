import argparse
from pathlib import Path

from phoenix.runner import read_jobq, run_job


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", "-j")
    args = parser.parse_args()

    print(args)
    var = read_jobq(Path(args.jobs))
    print(var)

    run_job(var)
