"""Build a single app image."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import toml
from cleez import Argument, Command
from cleez.colors import blue
from dictdiffer import diff
from pydantic import BaseModel


#
# Generic CLI boilerplate (copy/paster from "./validate.py")
#
class ValidateNgCommand(Command):
    """Validate one or more Nua configs."""

    name = "validate-ng"

    arguments = [
        Argument(
            "targets", nargs="+", help="Directories where to find the apps to validate"
        )
    ]

    def run(self, targets: list[str]):
        for target in targets:
            self._validate(Path(target))

    def _validate(self, target: Path):
        print(blue(f"Validating {target}..."))
        data = target.read_text()
        d = toml.loads(data)
        to_snake_cases(d)

        config = NuaConfig(**d)

        # This shows the diff between the original TOML and the parsed config once
        # it has been converted to a Pydantic model.
        # Pydantic doesn't check (AFAIK) for extra (just for missing keys or values
        # of the wrong type), so this is a way to check for typos in the keys, etc.
        for k, section, changes in diff(d, config.dict()):
            if len(changes) == 2 and not isinstance(changes[0], tuple):
                change_list = [changes]
            else:
                change_list = changes
            for kk, v in change_list:
                if v is None:
                    continue
                print(f"{k}: {section}.{kk}: {v}")


# --------------------------------------------------------------------


#
# This is the interesting part
#
class Metadata(BaseModel):
    id: str
    title: str
    author: str
    description: str | None
    tagline: str | None
    website: str | None
    version: str | None
    release: int | None
    license: str = "Proprietary"
    src_url: str | None
    src_checksum: str | None
    git_url: str | None
    git_branch: str | None
    checksum: str | None
    profile: str | list[str] | None
    tags: list[str] | None
    repo: str | None
    base_image: str | None

    # Notes:
    # - src_checksum and checksum should be merged


class Build(BaseModel):
    builder: str | dict | None
    builders: list[str] | list[dict] | None
    packages: str | list[str] | None
    test: str | list[str] | None
    before_build: str | list[str] | None
    build: str | list[str] | None

    # TBD
    document_root: str | None
    project: str | None
    meta_packages: str | list[str] | None

    # Deprecated
    build_packages: str | list[str] | None
    build_command: str | list[str] | None
    build_script: str | list[str] | None
    profiles: list[str] | None
    pip_install: str | list[str] | None
    node_version: str | None


class Run(BaseModel):
    packages: str | list[str] | None
    before_run: str | list[str] | None
    start: str | list[str] | None

    # Deprecated
    start_command: str | list[str] | None
    run_command: str | list[str] | None

    # Should the '[env]' section be here or at the root ?
    env: dict[str, Any] | None


class Resource(BaseModel):
    name: str
    type: str
    version: str | None

    # Probably obsolete
    service: str | None

    # TODO
    backup: Any


class Volume(BaseModel):
    name: str | None
    type: str | None
    prefix: str | None
    target: str | None
    source: str | None
    dst: str | None
    options: str | dict | None
    driver: str | None
    tmpfs_mode: str | None
    tmpfs_size: str | None
    # version: str | None
    # TODO
    backup: Any


class NuaConfig(BaseModel):
    metadata: Metadata
    build: Build | None
    run: Run | None
    env: dict[str, Any] | None
    resources: list[Resource] | None
    resource: list[Resource] | None
    volumes: list[Volume] | None
    volume: list[Volume] | None
    # TODO
    port: dict | None
    docker: dict | None
    # Should it be in `run` ?
    healthcheck: dict | None
    # Obsolete (?)
    instance: dict | None
    assign: dict | list | None


def to_snake_cases(d) -> None:
    """Converts all keys in a dict to snake_case, recursively, in place."""
    for key, value in list(d.items()):
        new_key = key.replace("-", "_")
        if new_key != key:
            d[new_key] = value
            del d[key]
        if isinstance(value, dict):
            to_snake_cases(value)
