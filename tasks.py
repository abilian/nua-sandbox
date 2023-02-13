import os
from pathlib import Path
from shutil import copy

import click
from abilian_devtools.invoke import import_tasks
from invoke import Context, task

NUA_AGENT_WHL = "nua-agent/dist/nua_agent-0.1-py3-none-any.whl"

SUB_REPOS = [
    "nua-agent",
    "nua-dev",
    "nua-run",
]

APPS = sorted(
    p.name
    for p in Path("apps").iterdir()
    if p.is_dir() and (p / "nua-config.toml").exists() and not (p / "SKIP").exists()
)


import_tasks(globals(), ["help"])

#
# Specific tasks
#
@task
def build_all(c: Context, no_cache=False, only="") -> None:
    """Build everyting in order."""
    build_base(c, no_cache=no_cache)
    build_apps(c, only=only)


@task
def build_base(c, no_cache=False):
    """Build base image only."""
    with c.cd("nua-agent"):
        c.run("poetry build")

    os.makedirs("base-image/dist", exist_ok=True)
    copy(NUA_AGENT_WHL, "base-image/dist/")

    with c.cd("base-image"):
        if no_cache:
            c.run("docker build --no-cache -t nua-base .", echo=True)
        else:
            c.run("docker build -t nua-base .", echo=True)


@task
def build_apps(c, only="", skip=""):
    """Build apps only."""
    if only:
        apps = [a.strip() for a in only.split(",")]
    else:
        apps = APPS
    apps = [a for a in apps if a not in skip.split(",")]

    print("Going to build apps:", ", ".join(apps))

    for app in apps:
        msg = f"Building app: {app}"
        print()
        click.secho(msg, fg="green")
        click.secho("=" * len(msg), fg="green")
        print()
        with c.cd(f"apps/{app}"):
            c.run("nua-dev build", echo=True)


#
# Generic tasks (copy/pasted)
#
@task
def install(c):
    """Install all sub-packages (and dependencies)"""
    run_in_subrepos(c, "pip install -e .")


@task
def lint(c):
    """Lint (static check) the whole project."""
    run_in_subrepos(c, "ruff src")
    run_in_subrepos(c, "mypy src")

    # c.run("ruff .")
    # c.run("pre-commit run --all-files")
    # run_in_subrepos(c, "adt all")


@task
def format(c):  # noqa: A001
    """Format the whole project."""
    run_in_subrepos(c, "black src && isort src")


@task
def test(c):
    """Run tests (in each subrepo)."""
    run_in_subrepos(c, "make test")


@task
def test_with_coverage(c):
    """Run tests with coverage (and combine results)."""
    run_in_subrepos(c, "pytest --cov nua")
    c.run("coverage combine */.coverage")
    # c.run("codecov --file .coverage")


@task
def mypy(c):
    """Run mypy (in each subrepo)."""
    run_in_subrepos(c, "mypy src")


@task
def pyright(c):
    """Run pyright (in each subrepo)."""
    run_in_subrepos(c, "pyright src")


@task
def clean(c):
    """Clean the whole project."""
    run_in_subrepos(c, "make clean")


@task
def fix(c):
    """Run ruff fixes in all subrepos."""
    run_in_subrepos(c, "ruff --fix src tests")


@task
def run(c, cmd):
    """Run given command in all subrepos."""
    run_in_subrepos(c, cmd)


@task
def update(c):
    """Update dependencies the whole project."""
    c.run("poetry update")
    run_in_subrepos(c, "poetry update && poetry install")


#
# Helpers
#
def h1(msg):
    print()
    print(msg)
    print("=" * len(msg))
    print()


def run_in_subrepos(c, cmd):
    for sub_repo in SUB_REPOS:
        h1(f"Running '{cmd}' in subrepos: {sub_repo}")
        with c.cd(sub_repo):
            c.run(cmd, echo=True)
