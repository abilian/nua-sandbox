"""Build a single app image."""

from __future__ import annotations

from pathlib import Path

from cleez import Argument, Command
from cleez.colors import blue, red

from nua_dev.config import Config, ConfigParseError
from nua_dev.utils.backports import chdir


class ValidateCommand(Command):
    """Validate one or more Nua configs."""

    name = "validate"

    arguments = [
        Argument(
            "targets", nargs="*", help="Directories where to find the apps to validate"
        )
    ]

    def run(self, targets: list[Path]):
        if not targets:
            targets = ["."]

        for target in targets:
            print(blue(f"Validating Nua config in: {target}"))
            with chdir(target):
                self._validate()

    def _validate(self):
        try:
            config = Config.from_path(".")
        except ConfigParseError as e:
            print(red(e))
            raise SystemExit(1)

        config.validate()
