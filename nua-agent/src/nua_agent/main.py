"""Manages the application lifecycle.

Build:

- `nua-agent build` builds the application.

Run (TODO, but not sure it's needed)

- start?
- stop?
- ?
"""
from __future__ import annotations

import json
from typing import Optional

import snoop
import typer
from typer import secho as echo
from typer.colors import YELLOW

from nua_agent.profiles import PROFILE_CLASSES
from nua_agent.system import install_packages

from . import sh, system
from .builder import Builder
from .util import Fail, print_version

snoop.install()
app = typer.Typer()


#
# Build lifecycle
#
@app.command()
def install_deps():
    """Install system dependencies."""
    build_config = json.load(open("_nua-build-config.json"))
    builder_name = build_config.get("builder")
    if not builder_name:
        echo("'builder' key not fount in config", fg=YELLOW)
        echo("(Build will proceed, but not be as efficient)")
        return

    for profile_cls in PROFILE_CLASSES:
        if profile_cls.name == builder_name:
            break
    else:
        raise Fail(f"Unknown builder {builder_name}")

    packages = set(profile_cls.builder_packages)

    packages.update(build_config.get("build-packages", []))

    install_packages(packages)


@app.command()
def build_app():
    """Build the application."""
    builder = Builder()

    try:
        builder.fetch_app_source()

        # Prepare the build environment
        # system.configure_apt()
        builder.prepare()
        system.clear_apt_cache()

        # Build the app
        builder.build_app()

        builder.cleanup()
    except Exception:
        raise Fail("An exception occurred")


@app.command()
def cleanup():
    """Clean up."""
    # Cleanup (or do we put this at the end of the build_app() function?)
    sh.rm("/root/.cache", recursive=True)
    sh.rm("/var/lib/apt", recursive=True)


# @app.command()
# def fetch_source():
#     """Fetch application source."""
#     builder = Builder()
#     builder.fetch_app_source()
#
#
# @app.command()
# def prepare():
#     """Setup build image."""
#     builder = Builder()
#     system.configure_apt()
#     builder.prepare()
#     system.clear_apt_cache()
#
#
# @app.command()
# def build():
#     """Build the application."""
#     builder = Builder()
#     builder.build()
#
#
# @app.command()
# def cleanup():
#     """Cleanup temp build arterfacts."""
#     builder = Builder()
#     sh.rm("/root/.cache", recursive=True)
#     sh.rm("/var/lib/apt", recursive=True)
#     builder.cleanup()


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
