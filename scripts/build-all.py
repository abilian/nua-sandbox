import argparse
import multiprocessing as mp
import subprocess
import time
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

from tabulate import tabulate

POOL_SIZE = 12


@dataclass(frozen=True, order=True)
class BuildResult:
    path: str
    command: str
    success: bool


@dataclass(frozen=True)
class BuildRunner:
    pool_size: int = POOL_SIZE
    report: bool = True

    def run(self):
        results = self.build_all()
        if self.report:
            self.report_results(results)

    def build_all(self) -> list[BuildResult]:
        apps = self.get_apps()
        apps = apps[0:4]
        with mp.Pool(self.pool_size) as pool:
            results = pool.map(self.try_build, apps)
        return results

    def get_apps(self):
        app_dirs = sorted(p for p in Path("apps").rglob("**") if self.is_nua_project(p))
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

        # for result in results:
        #     if result.success:
        #         table.append([result.path, "✅"])
        #     else:
        #         table.append([result.path, "❌"])
        print(tabulate(table, headers=["App"] + headers))

    def try_build(self, path: Path) -> BuildResult:
        try:
            # subprocess.run(["nua-build", path], check=True)
            subprocess.run(["nua-dev", "build", path], capture_output=True, check=True)
            return BuildResult(str(path), "nua-dev build", True)
        except subprocess.CalledProcessError:
            return BuildResult(str(path), "nua-dev build", False)

    def is_nua_project(self, path):
        if not path.is_dir():
            return False
        if (path / "nua-config.toml").exists():
            return True
        if (path / "nua" / "nua-config.toml").exists():
            return True
        return False


if __name__ == "__main__":
    t0 = time.time()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        nargs="?",
        action="store",
        default="run",
        help="Command to perform",
        choices=["run", "bench"],
    )

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
    parser.add_argument("-t", "--time", action="store_true", help="Print timing info")
    args = parser.parse_args()

    match args.command:
        case "run":
            build_runner = BuildRunner(pool_size=args.pool_size)
            build_runner.run()

            if args.time:
                t1 = time.time()
                print(f"Time: {t1 - t0:.2f} seconds")

        case "bench":
            for pool_size in range(1, 33):
                t0 = time.time()
                build_runner = BuildRunner(pool_size=pool_size, report=False)
                build_runner.run()
                t1 = time.time()
                print(f"CPUs: {pool_size} -> Time: {t1 - t0:.2f} seconds")
