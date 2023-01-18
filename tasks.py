import os
from shutil import copy

from invoke import task, Context

NUA_AGENT_WHL = "nua-agent/dist/nua_agent-0.1-py3-none-any.whl"

SUB_REPOS = [
    "nua-agent",
    "nua-dev",
]

@task
def build(c: Context) -> None:
    with c.cd("nua-agent"):
        c.run("poetry build")

    os.makedirs("base-image/dist", exist_ok=True)
    copy(NUA_AGENT_WHL, "base-image/dist/")

    with c.cd("base-image"):
        c.run("docker build -t nua-base .")

    with c.cd("apps/hedgedoc"):
        c.run("docker build -t nua-hedgedoc .")


@task
def install(c: Context) -> None:
    run_in_subrepos(c, "poetry install")


@task
def run(c, cmd):
    """Run given command in all subrepos."""
    run_in_subrepos(c, cmd)


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
            c.run(cmd)
