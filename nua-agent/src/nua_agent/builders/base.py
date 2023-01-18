from pathlib import Path

from ..config import read_config
from ..sh import shell
from ..types import JSON


class Builder:
    config: JSON

    builder_packages: list[str] = []

    def __init__(self, config: JSON = None):
        if config:
            self.config = config
        else:
            self.config = read_config()

    @property
    def app_id(self):
        return self.config["metadata"]["id"]

    @property
    def packages(self) -> list[str]:
        metadata = self.config["metadata"]

        packages = set()
        packages.update(metadata.get("build-packages", []))
        packages.update(metadata.get("run-packages", []))
        packages.update(self.builder_packages)

        return list(packages)

    def accept(self) -> bool:
        raise NotImplementedError

    def build(self):
        raise NotImplementedError

    def update_settings(self, settings):
        pass

    def fetch_app_source(self, strip_components=1):
        # TODO: rewrite in pure Python?
        # Cf. download_extract() in nua/lib/actions.py
        metadata = self.config["metadata"]
        src_url = metadata["src-url"]
        shell(f"curl -sL {src_url} | tar xz --strip-components={strip_components} -f -")

    def _check_files(self, files: list[str]) -> bool:
        """Return True if one of the files exists."""
        for file in files:
            if Path(file).exists():
                return True
        return False
