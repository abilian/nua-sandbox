from shutil import which

from cleez.colors import green


def found_app(kind):
    """Helper function to output app detected."""
    print(green(f"-----> {kind} app detected."))


def check_requirements(binaries) -> bool:
    """Checks if all the binaries exist and are executable."""
    print(green(f"-----> Checking requirements: {binaries}"))
    requirements = list(map(which, binaries))
    print(str(requirements))

    return None not in requirements
