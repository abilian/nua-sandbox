"""Build a single app image."""

from __future__ import annotations

import time
import traceback
from pathlib import Path

from cleez import Argument, Command
from cleez.colors import green, red

from nua_dev.builder import Builder
from nua_dev.config import Config, ConfigParseError
from nua_dev.utils.backports import chdir


class BuildCommand(Command):
    """Build one or more apps images."""

    name = "build"

    arguments = [
        Argument(
            "targets", nargs="*", help="Directories where to find the apps to build"
        )
    ]

    def run(self, targets: list[Path]):
        if not targets:
            targets = ["."]

        for target in targets:
            with chdir(target):
                self._build()

    def _build(self):
        """Build an image from the current directory."""
        t0 = time.time()
        try:
            config = Config.from_path(".")
        except ConfigParseError as e:
            print(red(e))
            raise SystemExit(1)

        try:
            builder = Builder(config)
            builder.build()
        except Exception as e:
            print(red(e))
            traceback.print_exc()
            raise SystemExit(1)
        finally:
            t1 = time.time()
            print(green(f"\nBuild took: {t1-t0:.2f}s"))
