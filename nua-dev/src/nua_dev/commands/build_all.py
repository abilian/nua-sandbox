import multiprocessing as mp
import subprocess
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from time import time as now

from cleez import Argument, Command, Option
from cleez.colors import green, red
from tabulate import tabulate

POOL_SIZE = 8
BUILD_METHODS = ["nua-build", "nua-dev"]


class BuildAllCommand(Command):
    name = "build-all"

    arguments = [
        Argument(
            "directory",
            nargs="?",
            action="store",
            default=".",
            help="Where to find the apps",
        ),
        Option(
            "-v",
            "--verbosity",
            default=0,
            action="count",
            help="Increase output verbosity",
        ),
        Option(
            "-p",
            "--pool-size",
            action="store",
            type=int,
            default=POOL_SIZE,
            help="Pool size",
        ),
        Option(
            "-d",
            "--cwd",
            action="store",
            default="",
            help="Change working directory",
        ),
        Option("-t", "--time", action="store_true", help="Print timing info"),
        Option("-b", "--bench", action="store_true", help="Run benchmarks"),
    ]

    def run(self, directory, verbosity, pool_size, cwd, time, bench):
        t0 = now()

        cwd = cwd or directory

        if bench:
            for pool_size in range(1, 33):
                t0 = now()
                build_runner = BuildRunner(
                    pool_size=pool_size, report=False, verbosity=verbosity
                )
                build_runner.run()
                t1 = now()
                print(f"CPUs: {pool_size} -> Time: {t1 - t0:.2f} seconds")

        else:
            build_runner = BuildRunner(
                pool_size=pool_size, cwd=cwd, verbosity=verbosity
            )
            build_runner.run()

            if time:
                t1 = now()
                print(f"Time: {t1 - t0:.2f} seconds")


@dataclass(frozen=True, order=True)
class BuildResult:
    path: str
    command: str
    success: bool
    duration: float


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
            return pool.starmap(self.try_build, args)

    def get_apps(self):
        return sorted(p for p in Path(self.cwd).rglob("**") if self.is_nua_project(p))

    def report_results(self, results):
        results.sort()

        headers = []
        table = []
        for k, g in groupby(results, lambda x: x.path):
            line = [k]
            headers = []
            for result in g:
                mark = {True: "✅", False: "❌"}[result.success]
                line.append(f"{mark} ({result.duration:.2f}s)")
                headers.append(result.command)
            table.append(line)

        print(tabulate(table, headers=["App", *headers]))

    def try_build(self, path: Path, command: str) -> BuildResult:
        t0 = now()
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

        t1 = now()
        return BuildResult(str(path), command, status, t1 - t0)

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
