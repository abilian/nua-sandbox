from pathlib import Path

from ..config import read_config
from ..types import JSON


class Builder:
    config: JSON

    def __init__(self, config: JSON = None):
        if config:
            self.config = config
        else:
            self.config = read_config()

    @property
    def app_id(self):
        return self.config["metadata"]["id"]

    # @property
    # def app_path(self):
    #     return join(APP_ROOT, self.app)

    def accept(self) -> bool:
        raise NotImplementedError

    def build(self):
        raise NotImplementedError

    def update_settings(self, settings):
        pass

    def _check_files(self, files: list[str]) -> bool:
        for file in files:
            if Path(file).exists():
                return True
        return False
