from __future__ import annotations

import json
from dataclasses import dataclass
from typing import cast

from nua_build_agent.types import JsonDict


def read_config() -> Config:
    return Config(json.load(open("_nua-config.json")))


@dataclass(frozen=True)
class Config:
    """Simplified version of the class in nua-dev/src/nua_dev/config.py."""

    _config: JsonDict

    def __getattr__(self, key):
        return self._config.get(key)

    def get(self, path, default=None):
        match path:
            case str():
                if "." in path:
                    return self.get(path.split("."), default)
                return self._config.get(path, default)
            case [*keys]:
                d = self._config
                for k in keys[0:-1]:
                    d = d.get(k, {})
                return d.get(keys[-1], default)
            case _:
                raise ValueError(f"Invalid path: {path}")

    def get_str(self, path, default="") -> str:
        return str(self.get(path, default))

    def get_dict(self, path, default=None) -> JsonDict:
        if default is None:
            default = {}
        return cast(dict, self.get(path, default))
