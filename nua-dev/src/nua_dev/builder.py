from __future__ import annotations

import json
from pathlib import Path

import json5
import jsonschema
import tomli
import typer
from tomli import TOMLDecodeError

from . import sh
from .sh import shell
from .types import JSON


class Builder:
    config: JSON = None

    def __init__(self) -> None:
        self.parse_config()

    def parse_config(self) -> None:
        typer.echo("Parsing config...")
        try:
            self.config = tomli.load(open("nua-config.toml", "rb"))
        except TOMLDecodeError as e:
            typer.echo(f"Error parsing nua-config.toml: {e}")
            raise typer.Exit(1)

        self.expand_src_url()
        self.validate_config()
        self.write_config()

    def expand_src_url(self):
        # Hack
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
            typer.echo(f"Error parsing nua-config.toml: {e.message}")
            raise typer.Exit(1)

    def write_config(self):
        # Write as JSON. From now on, we only use JSON.
        with Path("_nua-config.json").open("w") as fd:
            json.dump(self.config, fd, indent=2)

    def build(self):
        app_id = self.config["metadata"]["id"]
        sh.cp(Path(__file__).parent / "etc" / "Dockerfile", "Dockerfile.nua")
        shell(f"docker build -f Dockerfile.nua -t nua-{app_id} .")
