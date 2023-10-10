from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import jinja2
from cleez import Command, Option
from cleez.colors import blue
from github import Github, UnknownObjectException

from nua_dev.utils.console import Abort


class InitCommand(Command):
    """Initialize a new project, possibly from an existing GitHub
    repository."""

    name = "init"

    arguments = (
        Option("--from-github", help="GitHub repository to use as a template"),
        Option("--dir", help="Directory to create the project in"),
    )

    def run(self, from_github: str = "", dir: Path | None = None):
        """Initialize a new project."""
        if not from_github:
            raise Abort("Please specify a GitHub repository.")

        if from_github.endswith(".git"):
            from_github = from_github[:-4]
        if from_github.startswith("https:") or from_github.startswith("git@"):
            from_github = "/".join(from_github.split("/")[-2:])
        print(f"Using: {from_github}")

        ctx = GitHub(from_github).get_repo_info()
        template_file = Path(__file__).parent.parent / "etc" / "nua-config.toml.j2"
        template_str = template_file.read_text()
        environment = jinja2.Environment()
        template = environment.from_string(template_str)
        config_toml = template.render(project=ctx)

        if dir:
            os.chdir(dir)
        Path(ctx["id"]).mkdir(exist_ok=True)
        (Path(ctx["id"]) / "nua-config.toml").write_text(config_toml)


class GitHub:
    def __init__(self, repo_id) -> None:
        self.repo_id = repo_id

        print(blue(f"Initializing from GitHub: {self.repo_id}"))

        gh_token = os.getenv("GH_TOKEN")
        if not gh_token:
            raise Abort(
                "Please provide your GitHub access token as "
                + "the GH_TOKEN environment variable."
            )
        self.gh = Github(gh_token)

    def get_repo_info(self) -> dict[str, Any]:
        ctx = {}
        repo = self.gh.get_repo(self.repo_id)
        tags = list(repo.get_tags())
        if tags:
            tag = tags[0].name
            if tag.startswith("v"):
                version = tag[1:]
            else:
                version = tag
        else:
            tag = version = "???"

        try:
            license = repo.get_license().license.spdx_id
        except UnknownObjectException:
            license = "???"

        ctx["id"] = repo.name.lower()
        ctx["name"] = repo.name
        ctx["description"] = repo.description
        ctx["version"] = version
        if tag == "???":
            ctx["src_url"] = f"{repo.html_url}/archive/refs/heads/main.tar.gz"
        elif tag.startswith("v"):
            ctx["src_url"] = f"{repo.html_url}/archive/v{{version}}.tar.gz"
        else:
            ctx["src_url"] = f"{repo.html_url}/archive/{{version}}.tar.gz"
        ctx["license"] = license
        ctx["website"] = repo.homepage
        ctx["repo"] = repo.html_url
        return ctx
