from __future__ import annotations

import importlib.metadata
import os
from pathlib import Path
from typing import Any, Optional

import jinja2
import snoop
import typer
from github import Github
from typer.colors import GREEN, RED

from nua_dev.console import panic

from .builder import Builder

snoop.install()
app = typer.Typer()


@app.command()
def build():
    """Build image."""
    builder = Builder()
    try:
        builder.build()
    except Exception as e:
        typer.secho(e, fg=RED)
        raise typer.Exit(1)


@app.command()
def init(from_github: str = "", dir: Optional[Path] = None):
    """Initialize a new project."""
    if not from_github:
        panic("Please specify a GitHub repository.")

    ctx = get_repo_info(from_github)
    with (Path(__file__).parent / "etc" / "nua-config.toml.j2").open() as fd:
        environment = jinja2.Environment()
        template = environment.from_string(fd.read())
        config_toml = template.render(project=ctx)

    if dir:
        os.chdir(dir)
    Path(ctx["id"]).mkdir(exist_ok=True)
    with (Path(ctx["id"]) / "nua-config.toml").open("w") as fd:
        fd.write(config_toml)


def get_repo_info(from_github: str) -> dict[str, Any]:
    typer.secho(f"Initializing from GitHub: {from_github}", fg=GREEN)

    gh_token = os.getenv("GH_TOKEN")
    if not gh_token:
        panic("Please specify a GitHub repository.")

    gh = Github(gh_token)
    ctx = {}
    repo = gh.get_repo(from_github)
    tags = list(repo.get_tags())
    if tags:
        tag = tags[0].name
        if tag.startswith("v"):
            version = tag[1:]
        else:
            version = tag
    else:
        tag = version = "???"

    license = repo.get_license().license.spdx_id

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

    # pp(repo.description, repo.homepage, repo.html_url)
    # pp(list(repo.get_tags()))
    # pp(repo.get_license().content)


#
# Boilerplate
#
def _version_callback(value: bool) -> None:
    if value:
        print_version()
        raise typer.Exit(0)


def print_version():
    version = importlib.metadata.version("nua_agent")
    typer.echo(f"Nua Dev version: {version}")


OPTS = {
    "version": typer.Option(
        None,
        "--version",
        "-V",
        help="Show Nua version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
    "verbose": typer.Option(
        0, "--verbose", "-v", help="Show more informations, until -vvv.", count=True
    ),
    "color": typer.Option(True, "--color/--no-color", help="Colorize messages."),
}


@app.command()
def version():
    """Show version."""
    print_version()


def _usage():
    print_version()
    typer.echo("Usage: nua-agent [cmd]\n" "Try 'nua --help' for help.")
    raise typer.Exit(0)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = OPTS["version"],
):
    """Nua dev toolbox."""
    if ctx.invoked_subcommand is None:
        _usage()


if __name__ == "__main__":
    app()
