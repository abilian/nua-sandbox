from __future__ import annotations

import importlib.resources
import json
import tempfile
from pathlib import Path
from typing import Any

from attr import define, field
from cleez.colors import blue, green

from .config import Config
from .utils import sh
from .utils.backports import chdir

# Development version of the build agent wheel
BUILD_AGENT_WHEEL = "nua_build_agent-dev-py3-none-any.whl"


@define
class Builder:
    config: Config

    # Not used (yet)
    options: dict[str, Any] = field(factory=dict)

    @property
    def app_id(self) -> str:
        return self.config.app_id

    def build(self):
        temp_dir_prefix = f"{self.app_id}-build"
        build_dir = Path(tempfile.mkdtemp(prefix=temp_dir_prefix))
        print(blue(f"\nBuilding in {build_dir}"))
        self.build_in_tempdir(build_dir)
        print(green("\nDone. Cleaning up build dir"))

    def build_in_tempdir(self, build_dir: Path):
        self.setup_build_dir(build_dir)
        with chdir(build_dir):
            sh.shell(f"docker build -t nua-{self.app_id} .")

    def setup_build_dir(self, build_dir: Path):
        assert build_dir.is_dir()

        print(blue("Setting up build dir"))

        build_files = importlib.resources.files("nua_dev.etc.build_files")
        for file in build_files.iterdir():
            sh.cp(file, build_dir)

        self.write_config(build_dir)

        (build_dir / "dist").mkdir()
        if agent_wheel := self.get_agent_wheel():
            (build_dir / "dist" / BUILD_AGENT_WHEEL).write_bytes(agent_wheel)

        if self.config.get("build.src-url"):
            # Sources are downloaded by the build agent, no need to include them
            return

        (build_dir / "src").mkdir()
        src = self.config.get("build.src", ".")
        sh.cp(src, build_dir / "src", recursive=True)

        # FIXME: the dockerignore is relative to src dir, not the build dir
        # TODO: introduce ".nuaignore"?
        dockerignore_path = Path(src) / ".dockerignore"
        if dockerignore_path.exists():
            sh.cp(dockerignore_path, build_dir)

    def get_agent_wheel(self) -> bytes:
        """Returns a wheel for the agent package, or None if the agent sources
        are not available."""

        this_dir = Path(importlib.import_module("nua_dev").__path__[0])
        agent_src_root = this_dir.parent.parent.parent / "nua-build-agent"
        if not agent_src_root.exists():
            return b""

        print(blue(f"\nBuilding wheel for agent in {agent_src_root}"))
        with chdir(agent_src_root):
            sh.shell("poetry build")
            return next(Path("dist").glob("*.whl")).read_bytes()

    def write_config(self, build_dir: Path):
        # Write as JSON. From now on, we only use JSON.
        with (build_dir / "_nua-config.json").open("w") as fd:
            self.config.dump_to(fd)

        # TODO
        build_config = self.config.get_dict("build")
        with (build_dir / "_nua-build-config.json").open("w") as fd:
            json.dump(build_config, fd, indent=2)
