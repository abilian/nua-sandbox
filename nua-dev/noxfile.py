import nox
from nox import session

PYTHON_VERSIONS = ["3.10", "3.11"]

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = [
    "lint",
    "pytest",
]


@session
def lint(session: nox.Session):
    session.install("abilian-devtools")
    session.run("adt", "check")


@session(python=PYTHON_VERSIONS)
def pytest(session: nox.Session):
    session.install("-e", ".")
    session.install("pytest")
    # session.run("pip", "check")

    session.run("pytest", "tests", "src")
