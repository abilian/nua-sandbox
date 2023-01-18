"""
Manages the application lifecycle.

Build:

- pre-build
- fetch-source
- build

Run (TODO):

- start
- stop

"""
from __future__ import annotations

from typing import Optional

import typer

from . import system
from .builders import find_builder
from .builders.base import Builder
from .util import print_version

app = typer.Typer()


@app.command()
def pre_build():
    """Setup build image."""
    builder: Builder = find_builder()
    system.configure_apt()
    system.install_packages(builder.packages)
    system.clear_apt_cache()


@app.command()
def fetch_source():
    """Fetch application source."""
    builder: Builder = find_builder()
    builder.fetch_app_source()


@app.command()
def build():
    """Build the application."""
    builder = find_builder()
    builder.build()


#
# Boilerplate
#
def _version_callback(value: bool) -> None:
    if value:
        print_version()
        raise typer.Exit(0)


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
    """Nua agent (runs in containers)."""
    if ctx.invoked_subcommand is None:
        _usage()


if __name__ == "__main__":
    app()
