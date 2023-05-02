from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import json5
import jsonschema
import tomli
from attr import define
from tomli import TOMLDecodeError

from .types import JSON


class ConfigParseError(Exception):
    pass


@define
class Config:
    _config: JSON

    @classmethod
    def from_file(cls, path: Path | str) -> Config:
        if isinstance(path, str):
            path = Path(path)
        if path.is_dir():
            if (path / "nua-config.toml").exists():
                path /= "nua-config.toml"
            elif (path / "nua" / "nua-config.toml").exists():
                path = path / "nua" / "nua-config.toml"
            else:
                raise ConfigParseError(
                    f"Could not find nua-config.json or nua/nua-config.toml in {path}"
                )

        try:
            config = tomli.load(path.open("rb"))
        except TOMLDecodeError as e:
            raise ConfigParseError(f"Error parsing nua-config.toml: {e}")

        instance = cls(config)
        instance.add_defaults()
        instance.expand()
        instance.validate()
        return instance

    def __getattr__(self, key):
        return self._config.get(key)

    @property
    def app_id(self) -> str:
        return self._config["metadata"]["id"]

    def add_defaults(self):
        # Ad-hoc for now
        if "build" not in self._config:
            self._config["build"] = {}

    def expand(self):
        # Only src.url needs to be expanded for now, we'll expand
        # this as needed.
        self.expand_src_url()

    def expand_src_url(self):
        src_url = self._config["metadata"].get("src-url")
        if src_url and "{" in src_url:
            src_url = str.format(src_url, **self._config["metadata"])
            self._config["metadata"]["src-url"] = src_url

    def validate(self):
        schema_file = Path(__file__).parent / "etc" / "nua-config.schema.json5"
        schema = json5.load(schema_file.open("rb"))
        try:
            jsonschema.validate(self._config, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ConfigParseError(f"Error parsing nua-config.toml: {e.message}")

    def write_config(self):
        # Write as JSON. From now on, we only use JSON.
        with Path("_nua-config.json").open("w") as fd:
            self.dump_to(fd)

    def dump_to(self, fd, sections=Optional[list[str]]):
        if sections is None:
            json.dump(self._config, fd, indent=2)
        else:
            # Assume sections == ["metadata", "build"] for now
            d = {
                "metadata": self._config["metadata"],
                "build": self._config["build"],
            }
            json.dump(d, fd, indent=2)
