import nox

PYTHON_VERSIONS = ["3.10", "3.11"]

nox.options.reuse_existing_virtualenvs = True

nox.options.sessions = [
    "lint",
    "pytest",
]

SUB_REPOS = [
    "nua-dev",
    "nua-build-agent",
    # "nua-run",
]


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("sub_repo", SUB_REPOS)
def pytest(session: nox.Session, sub_repo: str):
    run_subsession(session, sub_repo)


@nox.session
@nox.parametrize("sub_repo", SUB_REPOS)
def lint(session: nox.Session, sub_repo: str):
    run_subsession(session, sub_repo)


@nox.session(name="update-deps")
def update_deps(session: nox.Session):
    for sub_repo in SUB_REPOS:
        with session.chdir(sub_repo):
            session.run("poetry", "install", external=True)
            session.run("poetry", "update", external=True)
        print()


def run_subsession(session, sub_repo):
    name = session.name.split("(")[0]
    print(f"\nRunning session: {session.name} in subrepo: {sub_repo}\n")
    with session.chdir(sub_repo):
        session.run("nox", "-e", name, external=True)
    print()
