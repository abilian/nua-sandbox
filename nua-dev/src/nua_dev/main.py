from __future__ import annotations

import importlib.metadata
import os
import time
import traceback
from pathlib import Path
from typing import Optional

import jinja2
import snoop
import typer
from typer.colors import GREEN, RED

from nua_dev import upstream
from nua_dev.backports import chdir
from nua_dev.config import Config
from nua_dev.console import panic

from .builder import Builder

snoop.install()
app = typer.Typer()


@app.command()
def build(targets: list[Path]):
    """Build image(s)."""
    if not targets:
        _build()
        return

    for target in targets:
        with chdir(target):
            _build()


def _build():
    """Build an image from the current directory."""
    t0 = time.time()
    try:
        config = Config().parse_config()
        builder = Builder(config)
        builder.build()
    except Exception as e:
        typer.secho(e, fg=RED)
        traceback.print_exc()
        raise typer.Exit(1)
    finally:
        t1 = time.time()
        typer.secho(f"\nBuild took: {t1-t0:.2f}s", fg=GREEN)


@app.command()
def init(from_github: str = "", dir: Optional[Path] = None):
    """Initialize a new project."""
    if not from_github:
        panic("Please specify a GitHub repository.")

    ctx = upstream.GitHub(from_github).get_repo_info()
    with (Path(__file__).parent / "etc" / "nua-config.toml.j2").open() as fd:
        environment = jinja2.Environment()
        template = environment.from_string(fd.read())
        config_toml = template.render(project=ctx)

    if dir:
        os.chdir(dir)
    Path(ctx["id"]).mkdir(exist_ok=True)
    with (Path(ctx["id"]) / "nua-config.toml").open("w") as fd:
        fd.write(config_toml)


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
