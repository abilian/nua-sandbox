from __future__ import annotations

import os
from typing import Any

import typer
from github import Github, UnknownObjectException
from typer.colors import GREEN

from nua_dev.console import panic


class GitHub:
    def __init__(self, repo_id) -> None:
        self.repo_id = repo_id

        typer.secho(f"Initializing from GitHub: {self.repo_id}", fg=GREEN)

        gh_token = os.getenv("GH_TOKEN")
        if not gh_token:
            panic(
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
        return ctx
