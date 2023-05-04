from __future__ import annotations

import json
from pathlib import Path
from typing import BinaryIO, Optional, cast

import json5
import jsonschema
import tomli
from attr import define
from tomli import TOMLDecodeError

from .types import JsonDict


class ConfigParseError(Exception):
    pass


@define
class Config:
    _config: JsonDict

    @classmethod
    def from_dict(cls, config: JsonDict) -> Config:
        instance = cls(config)
        instance.add_defaults()
        instance.expand()
        instance.validate()
        return instance

    @classmethod
    def from_file(cls, file: BinaryIO) -> Config:
        try:
            config = tomli.load(file)
        except TOMLDecodeError as e:
            raise ConfigParseError(f"Error parsing nua-config.toml: {e}")

        return cls.from_dict(config)

    @classmethod
    def from_path(cls, path: Path | str) -> Config:
        if isinstance(path, str):
            path = Path(path)
        if path.is_dir():
            if (path / "nua-config.toml").exists():
                path /= "nua-config.toml"
            elif (path / "nua" / "nua-config.toml").exists():
                path = path / "nua" / "nua-config.toml"
            else:
                abs_path = path.resolve()
                raise ConfigParseError(
                    f"Could not find nua-config.json "
                    f"or nua/nua-config.toml in {abs_path}"
                )

        file = path.open("rb")
        return cls.from_file(file)

    def __getattr__(self, key):
        return AttrGetter(self._config).get(key)

    @property
    def app_id(self) -> str:
        return self.get_str("metadata.id")

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


MARK = object()


# This is probably not a good idea (or it needs to be done differently)
@define
class AttrGetter:
    _dict: dict

    def get(self, key: str, default=MARK):
        value = self._dict.get(key, default)
        if value is MARK:
            raise AttributeError(f"Attribute {key} not found")

        if isinstance(value, dict):
            return AttrGetter(value)
        else:
            return value

    def __getattr__(self, key):
        return self.get(key)
