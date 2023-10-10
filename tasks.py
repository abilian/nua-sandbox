from pathlib import Path

from invoke import Context, task

NUA_AGENT_WHL = "nua-build-agent/dist/nua_agent-0.1-py3-none-any.whl"

SUB_REPOS = [
    "nua-build-agent",
    "nua-dev",
    "nua-run",
]

APPS = sorted(
    p.name
    for p in Path("apps").iterdir()
    if p.is_dir() and (p / "nua-config.toml").exists() and not (p / "SKIP").exists()
)

try:
    from click import secho
except ImportError:
    secho = None


def echo(msg, **kwargs):
    if secho:
        secho(msg, **kwargs)
    else:
        print(msg)


try:
    from abilian_devtools.invoke import import_tasks

    import_tasks(globals(), ["help"])
except ImportError:
    print("Warning: abilian_devtools not installed, 'invoke help' won't work.")
    pass


#
# Specific tasks
#
@task
def build_all(c: Context, only="", skip=""):
    """Build all apps (or maybe not)."""
    if only:
        apps = [a.strip() for a in only.split(",")]
    else:
        apps = APPS
    apps = [a for a in apps if a not in skip.split(",")]

    print("Going to build apps:", ", ".join(apps))

    for app in apps:
        msg = f"Building app: {app}"
        print()
        echo(msg, fg="green")
        echo("=" * len(msg), fg="green")
        print()
        with c.cd(f"apps/{app}"):
            c.run("nua-dev build .", echo=True)


@task
def build(c: Context, app):
    """Build one single app."""

    msg = f"Building app: {app}"
    print()
    echo(msg, fg="green")
    echo("=" * len(msg), fg="green")
    print()
    with c.cd(f"apps/{app}"):
        c.run("nua-dev build .", echo=True)


#
# Generic tasks (copy/pasted)
#
@task
def install(c: Context):
    """Install all sub-packages (and dependencies)"""
    run_in_subrepos(c, "pip install -e .")


@task
def lint(c: Context):
    """Lint (static check) the whole project."""
    run_in_subrepos(c, "ruff src")
    run_in_subrepos(c, "mypy src")

    # c.run("ruff .")
    # c.run("pre-commit run --all-files")
    # run_in_subrepos(c, "adt all")


@task
def format(c: Context):  # noqa: A001
    """Format the whole project."""
    run_in_subrepos(c, "black src && isort src")


@task
def test(c: Context):
    """Run tests (in each subrepo)."""
    run_in_subrepos(c, "make test")


@task
def test_with_coverage(c: Context):
    """Run tests with coverage (and combine results)."""
    run_in_subrepos(c, "pytest --cov nua")
    c.run("coverage combine */.coverage")
    # c.run("codecov --file .coverage")


@task
def mypy(c: Context):
    """Run mypy (in each subrepo)."""
    run_in_subrepos(c, "mypy src")


@task
def pyright(c: Context):
    """Run pyright (in each subrepo)."""
    run_in_subrepos(c, "pyright src")


@task
def clean(c: Context):
    """Clean the whole project."""
    run_in_subrepos(c, "make clean")


@task
def fix(c: Context):
    """Run ruff fixes in all subrepos."""
    run_in_subrepos(c, "ruff --fix src tests")


@task
def run(c: Context, cmd):
    """Run given command in all subrepos."""
    run_in_subrepos(c, cmd)


@task
def update(c: Context):
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
