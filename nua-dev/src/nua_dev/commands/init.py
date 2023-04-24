from __future__ import annotations

import os
from pathlib import Path

import jinja2
from cleez import Argument, Command

from nua_dev import upstream
from nua_dev.console import panic


class InitCommand(Command):
    """Initialize a new project, possibly from an existing GitHub repository."""

    name = "init"

    arguments = [
        Argument("--from-github", help="GitHub repository to use as a template"),
        Argument("--dir", help="Directory to create the project in"),
    ]

    def run(self, from_github: str = "", dir: Path | None = None):
        """Initialize a new project."""
        if not from_github:
            panic("Please specify a GitHub repository.")

        ctx = upstream.GitHub(from_github).get_repo_info()
        template_file = Path(__file__).parent.parent / "etc" / "nua-config.toml.j2"
        template_str = template_file.read_text()
        environment = jinja2.Environment()
        template = environment.from_string(template_str)
        config_toml = template.render(project=ctx)

        if dir:
            os.chdir(dir)
        Path(ctx["id"]).mkdir(exist_ok=True)
        (Path(ctx["id"]) / "nua-config.toml").write_text(config_toml)
