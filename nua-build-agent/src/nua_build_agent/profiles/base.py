from pathlib import Path
from typing import cast

from ..config import Config
from ..types import JsonDict


class BaseProfile:
    config: Config

    name: str = ""
    label: str = ""
    builder_packages: list[str] = []

    def __init__(self, config: Config):
        self.config = config

    @property
    def app_id(self):
        metadata = cast(dict, self.config["metadata"])
        return metadata["id"]

    #
    # Lifecycle methods (called from `../builder.py`)
    #
    def accept(self) -> bool:
        """Must be implemented in subclasses."""
        raise NotImplementedError

    def check(self) -> bool:
        """Check if the environment is ready."""
        return True

    def prepare(self):
        """Prepare the build: additional specific steps, if needed.

        Does nothing by default.
        """
        pass

    def build(self):
        """Must be implemented in subclasses."""
        raise NotImplementedError

    def cleanup(self):
        """Cleanup after the build.

        Does nothing by default.
        """
        pass

    #
    # Helpers
    #
    def get_system_packages(self) -> list[str]:
        default_build: JsonDict = {}
        build_info: JsonDict = self.config.get_dict("build", default_build)

        packages: set[str] = set()
        packages.update(cast(list[str], build_info.get("packages", [])))
        # packages.update(cast(list[str], build_info.get("run-packages", [])))
        packages.update(self.builder_packages)

        return list(packages)

    # def update_settings(self, settings):
    #     pass

    def _check_files(self, files: list[str]) -> bool:
        """Return True if one of the files exists."""
        for file in files:
            if Path(file).exists():
                return True
        return False
