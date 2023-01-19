from pathlib import Path

from ..types import JSON


class BaseProfile:
    config: JSON

    builder_packages: list[str] = []
    label: str = ""

    def __init__(self, config: JSON):
        self.config = config

    @property
    def app_id(self):
        return self.config["metadata"]["id"]

    def get_system_packages(self) -> list[str]:
        metadata = self.config["metadata"]

        packages = set()
        packages.update(metadata.get("build-packages", []))
        packages.update(metadata.get("run-packages", []))
        packages.update(self.builder_packages)

        return list(packages)

    def install_extra_packages(self):
        """Implemented in subclasses, if needed."""
        pass

    def accept(self) -> bool:
        """Implemented in subclasses"""
        raise NotImplementedError

    def build(self):
        """Implemented in subclasses"""
        raise NotImplementedError

    def _pre_build(self):
        """Pre-build check. Not used yet."""
        raise NotImplementedError

    # def update_settings(self, settings):
    #     pass

    def _check_files(self, files: list[str]) -> bool:
        """Return True if one of the files exists."""
        for file in files:
            if Path(file).exists():
                return True
        return False
