from __future__ import annotations

import time
import traceback
from pathlib import Path

from cleez import Argument, Command
from cleez.colors import green, red

from nua_dev.backports import chdir
from nua_dev.builder import Builder
from nua_dev.config import Config, ConfigParseError


class BuildCommand(Command):
    name = "build"

    arguments = [
        Argument("targets", nargs="+", help="Files or directories to check"),
    ]

    def run(self, targets: list[Path]):
        """Build image(s)."""
        if not targets:
            self._build()
            return

        for target in targets:
            with chdir(target):
                self._build()

    def _build(self):
        """Build an image from the current directory."""
        t0 = time.time()
        try:
            config = Config.from_file(".")
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
