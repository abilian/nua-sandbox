"""Build all the apps in a given directory.

Useful for tests and benchmarks.
"""

import argparse
import multiprocessing as mp
import subprocess
from dataclasses import dataclass, field
from itertools import groupby
from pathlib import Path
from time import time as now

from cleez import Argument, Command, Option
from cleez.actions import COUNT, STORE, STORE_TRUE
from cleez.colors import green, red
from tabulate import tabulate

POOL_SIZE = 8
BUILD_METHODS = ["nua-build", "nua-dev"]


class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(","))


class BuildAllCommand(Command):
    name = "build-all"

    arguments = [
        Argument(
            "directory",
            nargs="?",
            action=STORE,
            default=".",
            help="Where to find the apps",
        ),
        Option(
            "-v",
            "--verbosity",
            default=0,
            action=COUNT,
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
            action=STORE,
            default="",
            help="Change working directory",
        ),
        Option(
            "-B",
            "--build-methods",
            action=SplitArgs,
            help="Build method(s) to use (comma-separated)",
        ),
        Option("-t", "--time", action=STORE_TRUE, help="Print timing info"),
        Option("-b", "--bench", action=STORE_TRUE, help="Run benchmarks"),
    ]

    def run(
        self, _args, directory, build_methods, verbosity, pool_size, cwd, time, bench
    ):
        cwd = cwd or directory
        build_methods = build_methods or BUILD_METHODS

        if bench:
            self.run_bench(verbosity, cwd)
        else:
            self.run_build(build_methods, verbosity, pool_size, cwd, time)

    def run_build(self, build_methods, verbosity, pool_size, cwd, time):
        t0 = now()

        build_runner = BuildRunner(
            build_methods=build_methods,
            pool_size=pool_size,
            cwd=cwd,
            verbosity=verbosity,
        )
        build_runner.run()

        if time:
            t1 = now()
            print(f"Time: {t1 - t0:.2f} seconds")

    def run_bench(self, verbosity, cwd):
        for pool_size in range(1, 33):
            t0 = now()
            build_runner = BuildRunner(
                cwd=cwd, pool_size=pool_size, report=False, verbosity=verbosity
            )
            build_runner.run()
            t1 = now()
            print(f"CPUs: {pool_size} -> Time: {t1 - t0:.2f} seconds")


@dataclass(frozen=True, order=True)
class BuildResult:
    path: str
    command: str
    success: bool
    duration: float


@dataclass(frozen=True)
class BuildRunner:
    cwd: str = "."
    build_methods: list[str] = field(default_factory=lambda: BUILD_METHODS)
    pool_size: int = POOL_SIZE
    report: bool = True
    verbosity: int = 0

    def run(self):
        self.validate()
        results = self.build_all()
        if self.report:
            self.report_results(results)

    def validate(self):
        for bm in self.build_methods:
            if bm not in BUILD_METHODS:
                raise ValueError(f"Invalid build method: {bm}")

    def build_all(self) -> list[BuildResult]:
        apps = self.get_apps()
        args = [(app, method) for app in apps for method in self.build_methods]

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

    def try_build(self, path: Path, method: str) -> BuildResult:
        t0 = now()
        self.log(f"Starting build of {path} with {method}", 1)

        match method:
            case "nua-build":
                args = ["nua-build", "--no-save", str(path)]
            case "nua-dev":
                args = ["nua-dev", "build", str(path)]
            case _:
                raise ValueError(f"Unknown command: {method}")

        try:
            subprocess.run(args, capture_output=True, check=True)
            status = True
            self.log(f"Build of {path} with {method} succeeded", 1, green)
        except subprocess.CalledProcessError:
            status = False
            self.log(f"Build of {path} with {method} failed", 1, red)

        t1 = now()
        return BuildResult(str(path), method, status, t1 - t0)

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
