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
        build_info = self.config.get("build", {})

        packages = set()
        packages.update(build_info.get("build-packages", []))
        packages.update(build_info.get("run-packages", []))
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
