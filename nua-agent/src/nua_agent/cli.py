"""Manages the application lifecycle.

Build:

- `nua-agent build` builds the application.

Run (TODO, but not sure it's needed)

- start?
- stop?
- ?
"""
from __future__ import annotations

import importlib.metadata
import json

import snoop
from cleez import CLI, Command
from cleez.actions import VERSION
from cleez.colors import yellow

from . import sh, system
from .builder import Builder
from .profiles import PROFILE_CLASSES
from .system import install_packages
from .util import Fail

snoop.install()


#
# Build lifecycle
#
class InstallDeps(Command):
    """Install system dependencies."""

    name = "install-deps"

    def run(self):
        build_config = json.load(open("_nua-build-config.json"))
        builder_name = build_config.get("builder")
        if not builder_name:
            print(yellow("'builder' key not fount in config"))
            print("(Build will proceed, but not be as efficient)")
            return

        if "-" in builder_name:
            builder_name = builder_name.split("-")[0]

        for profile_cls in PROFILE_CLASSES:
            if profile_cls.name == builder_name:
                break
        else:
            raise Fail(f"Unknown builder {builder_name}")

        packages = set(profile_cls.builder_packages)

        packages.update(build_config.get("build-packages", []))

        install_packages(packages)


class BuildApp(Command):
    """Build the application."""

    name = "build-app"

    def run(self):
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


class Cleanup(Command):
    """Clean up."""

    name = "cleanup"

    def run(self):
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


def get_cli() -> CLI:
    cli = CLI("nua-agent", version=importlib.metadata.version("nua-agent"))
    cli.add_option(
        "-V",
        "--version",
        action=VERSION,
        version=cli.version,
        help="Show version and exit.",
    )
    cli.add_command(InstallDeps)
    cli.add_command(BuildApp)
    cli.add_command(Cleanup)
    return cli


def main():
    cli = get_cli()
    cli.run()
