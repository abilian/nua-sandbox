from __future__ import annotations

import importlib.metadata
import os
import stat
import subprocess as sp
import sys
from pathlib import Path
from textwrap import dedent
from typing import Optional

import snoop
import typer

snoop.install()
app = typer.Typer()

# pp(sys.argv)


NUA_ROOT = Path("/home/nua")
GIT_ROOT = NUA_ROOT / "repos"
APPS_ROOT = NUA_ROOT / "apps"
NUA_GIT_SCRIPT = NUA_ROOT / "venv" / "bin" / "nua-git"


#
# Commands
#
@app.command()
def git_hook(app_name: str):
    """Post-receive git hook."""
    app = sanitize_app_name(app_name)
    repo_path = GIT_ROOT / app
    app_path = APPS_ROOT / app

    for line in sys.stdin:
        _oldrev, newrev, _refname = line.strip().split(" ")

        # Handle pushes
        if not app_path.exists():
            typer.secho(f"-----> Creating app '{app:s}'", fg="green")
            app_path.mkdir(parents=True)
            cmd = ["git", "clone", "--quiet", str(repo_path), str(app)]
            sp.run(cmd, cwd=APPS_ROOT)

        _run_build(app, newrev=newrev)
        # run_deploy(app, newrev=newrev)


def _run_build(app, newrev):
    """Build an app by resetting the work directory."""
    app_path = APPS_ROOT / app

    env = {"GIT_WORK_DIR": app_path}
    if not app_path.exists():
        typer.secho(f"Error: app '{app}' not found.", fg="red")

    typer.secho(f"-----> Deploying app '{app}'", fg="green")
    sp.run("git fetch --quiet", cwd=app_path, env=env, shell=True)
    if newrev:
        sp.run(f"git reset --hard {newrev}", cwd=app_path, env=env, shell=True)
    sp.run("git submodule init", cwd=app_path, env=env, shell=True)
    sp.run("git submodule update", cwd=app_path, env=env, shell=True)

    # Todo: call nua-build or something...


@app.command()
def git_receive_pack(app_name: str):
    """Handle git pushes for an app."""
    app = sanitize_app_name(app_name)
    hook_path = GIT_ROOT / app / "hooks" / "post-receive"

    if not hook_path.exists():
        _create_hook(app, hook_path)

    # Handle the actual receive. Will be called with 'git-hook' after it happens.
    cmd = ["git-receive-pack", app]
    sp.run(cmd, cwd=GIT_ROOT)


def _create_hook(app, hook_path):
    hook_path.parent.mkdir(parents=True, exist_ok=True)

    # Initialize the repository with a hook to this script
    sp.run(["git", "init", "--quiet", "--bare", app], cwd=GIT_ROOT)
    with hook_path.open("w") as h:
        h.write(
            dedent(
                f"""\
                #!/usr/bin/env bash
                set -e; set -o pipefail;
                NUA_ROOT="{NUA_ROOT}" {NUA_GIT_SCRIPT} git-hook {app}
                """
            )
        )
    # Make the hook executable by our user
    hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR)


@app.command()
def shell():
    """Start a shell on the Nua server."""
    print("Starting shell...")
    os.execl("/bin/bash", "/bin/bash")


#
# Utilities
#
def sanitize_app_name(app: str) -> str:
    """Sanitize the app name and build matching path."""
    app = (
        "".join(c for c in app if c.isalnum() or c in (".", "_", "-"))
        .rstrip()
        .lstrip("/")
    )
    return app


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
    """nua-git (internal) utilities."""
    if ctx.invoked_subcommand is None:
        os.execl("/bin/bash", "/bin/bash")
