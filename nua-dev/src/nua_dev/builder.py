from __future__ import annotations

import json
import tempfile
from os import mkdir
from pathlib import Path
from typing import Any

from attr import define, field
from typer import secho as echo
from typer.colors import CYAN, GREEN

from . import sh
from .backports import chdir
from .types import JSON


@define
class Builder:
    config: JSON = None
    # Not used (yet)
    options: dict[str, Any] = field(factory=dict)

    @property
    def app_id(self) -> str:
        return self.config["metadata"]["id"]  # type: ignore

    def build(self):
        self._build_agent()
        temp_dir_prefix = f"{self.app_id}-build"

        build_dir = tempfile.mkdtemp(prefix=temp_dir_prefix)

        echo(f"\nBuilding in {build_dir}", fg=GREEN)
        with chdir(build_dir):
            self.setup_build_dir()
            sh.shell(f"docker build -t nua-{self.app_id} .")

        echo("\nCleaning up build dir", fg=GREEN)

    def setup_build_dir(self):
        echo("Setting up build dir", fg=CYAN)
        etc_dir = Path(__file__).parent / "etc"
        for file in etc_dir.glob("build_files/*"):
            sh.cp(file, ".")
        self.write_config()
        agent_wheel = list((self.agent_root / "dist").glob("*.whl"))[0]
        mkdir("dist")
        sh.cp(agent_wheel, "dist")

    @property
    def agent_root(self) -> Path:
        import nua_dev

        return Path(nua_dev.__file__).parent.parent.parent.parent / "nua-agent"

    def _build_agent(self):
        echo("\nBuilding wheel for agent", fg=GREEN)
        with chdir(self.agent_root):
            sh.shell("poetry build")

    def write_config(self):
        # Write as JSON. From now on, we only use JSON.
        with Path("_nua-config.json").open("w") as fd:
            json.dump(self.config, fd, indent=2)

        build_config = self.config["build"]
        with Path("_nua-build-config.json").open("w") as fd:
            json.dump(build_config, fd, indent=2)
