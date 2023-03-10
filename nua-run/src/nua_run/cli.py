from __future__ import annotations

import importlib.metadata
from typing import Optional

import snoop
import typer

snoop.install()
app = typer.Typer()


#
# Nothing there (yet)
#


#
# Boilerplate
#
def _version_callback(value: bool) -> None:
    if value:
        print_version()
        raise typer.Exit(0)


def print_version():
    version = importlib.metadata.version("nua_run")
    typer.echo(f"nua-run version: {version}")


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
    typer.echo("Usage: nua-run [cmd]\n" "Try 'nua --help' for help.")
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
