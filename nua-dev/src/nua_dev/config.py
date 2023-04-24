from __future__ import annotations

import json
from pathlib import Path

import json5
import jsonschema
import tomli
from tomli import TOMLDecodeError

from nua_dev.types import JSON


class ConfigParseError(Exception):
    pass


class Config:
    config: JSON

    def parse_config(self, path: Path | str = ".") -> JSON:
        if isinstance(path, str):
            path = Path(path)
        print(f"Parsing config in {path}...")
        if path.is_dir():
            path /= "nua-config.toml"
        try:
            self.config = tomli.load(path.open("rb"))
        except TOMLDecodeError as e:
            raise ConfigParseError(f"Error parsing nua-config.toml: {e}")

        self.add_defaults()

        self.expand()
        self.validate_config()
        return self.config

    def add_defaults(self):
        # Ad-hoc for now
        if "build" not in self.config:
            self.config["build"] = {}

    def expand(self):
        # Only src.url needs to be expanded for now, we'll expand
        # this as needed.
        self.expand_src_url()

    def expand_src_url(self):
        src_url = self.config["metadata"].get("src-url")
        if src_url and "{" in src_url:
            src_url = str.format(src_url, **self.config["metadata"])
            self.config["metadata"]["src-url"] = src_url

    def validate_config(self):
        schema_file = Path(__file__).parent / "etc" / "nua-config.schema.json5"
        schema = json5.load(schema_file.open("rb"))
        try:
            jsonschema.validate(self.config, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ConfigParseError(f"Error parsing nua-config.toml: {e.message}")

    def write_config(self):
        # Write as JSON. From now on, we only use JSON.
        with Path("_nua-config.json").open("w") as fd:
            json.dump(self.config, fd, indent=2)
