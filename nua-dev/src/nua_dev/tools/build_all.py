import argparse
import multiprocessing as mp
import subprocess
import time
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

from cleez.colors import green, red
from tabulate import tabulate

POOL_SIZE = 8
BUILD_METHODS = ["nua-build", "nua-dev"]


@dataclass(frozen=True, order=True)
class BuildResult:
    path: str
    command: str
    success: bool


@dataclass(frozen=True)
class BuildRunner:
    pool_size: int = POOL_SIZE
    report: bool = True
    cwd: str = "."
    verbosity: int = 0

    def run(self):
        results = self.build_all()
        if self.report:
            self.report_results(results)

    def build_all(self) -> list[BuildResult]:
        apps = self.get_apps()
        args = [(app, cmd) for app in apps for cmd in BUILD_METHODS]

        with mp.Pool(self.pool_size) as pool:
            results = pool.starmap(self.try_build, args)
        return results

    def get_apps(self):
        app_dirs = sorted(
            p for p in Path(self.cwd).rglob("**") if self.is_nua_project(p)
        )
        return app_dirs

    def report_results(self, results):
        results.sort()

        headers = []
        table = []
        for k, g in groupby(results, lambda x: x.path):
            line = [k]
            headers = []
            for result in g:
                line.append("✅" if result.success else "❌")
                headers.append(result.command)
            table.append(line)

        print(tabulate(table, headers=["App"] + headers))

    def try_build(self, path: Path, command: str) -> BuildResult:
        self.log(f"Starting build of {path} with {command}", 1)
        match command:
            case "nua-build":
                args = ["nua-build", str(path)]
            case "nua-dev":
                args = ["nua-dev", "build", str(path)]
            case _:
                raise ValueError(f"Unknown command: {command}")

        try:
            subprocess.run(args, capture_output=True, check=True)
            status = True
            self.log(f"Build of {path} with {command} succeeded", 1, green)
        except subprocess.CalledProcessError:
            status = False
            self.log(f"Build of {path} with {command} failed", 1, red)

        return BuildResult(str(path), command, status)

    def is_nua_project(self, path):
        if not path.is_dir():
            return False
        if path.name == "nua":
            return False
        if (path / "nua-config.toml").exists():
            return True
        if (path / "nua" / "nua-config.toml").exists():
            return True
        return False

    def log(self, msg, level=0, color=None):
        if self.verbosity >= level:
            if color:
                msg = color(msg)
            print(msg)


def main():
    t0 = time.time()

    parser = argparse.ArgumentParser()

    # Arguments
    parser.add_argument(
        "directory",
        nargs="?",
        action="store",
        default=".",
        help="Where to find the apps",
    )

    # Options
    parser.add_argument(
        "-v", "--verbosity", default=0, action="count", help="Increase output verbosity"
    )
    parser.add_argument(
        "-p",
        "--pool-size",
        action="store",
        type=int,
        default=POOL_SIZE,
        help="Pool size",
    )
    parser.add_argument(
        "-d",
        "--cwd",
        action="store",
        default="",
        help="Change working directory",
    )
    parser.add_argument("-t", "--time", action="store_true", help="Print timing info")
    parser.add_argument("-b", "--bench", action="store_true", help="Run benchmarks")

    args = parser.parse_args()
    cwd = args.cwd or args.directory

    if args.bench:
        for pool_size in range(1, 33):
            t0 = time.time()
            build_runner = BuildRunner(
                pool_size=pool_size, report=False, verbosity=args.verbosity
            )
            build_runner.run()
            t1 = time.time()
            print(f"CPUs: {pool_size} -> Time: {t1 - t0:.2f} seconds")

    else:
        build_runner = BuildRunner(
            pool_size=args.pool_size, cwd=cwd, verbosity=args.verbosity
        )
        build_runner.run()

        if args.time:
            t1 = time.time()
            print(f"Time: {t1 - t0:.2f} seconds")


if __name__ == "__main__":
    main()
