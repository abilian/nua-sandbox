from shutil import which

from click import secho as echo


def found_app(kind):
    """Helper function to output app detected."""
    echo(f"-----> {kind} app detected.", fg="green")


def check_requirements(binaries) -> bool:
    """Checks if all the binaries exist and are executable."""

    echo(f"-----> Checking requirements: {binaries}", fg="green")
    requirements = list(map(which, binaries))
    echo(str(requirements))

    return None not in requirements
