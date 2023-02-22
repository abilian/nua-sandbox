import os

from click import secho
from typer.colors import GREEN

from .sh import shell

os.environ["DEBIAN_FRONTEND"] = "noninteractive"


def install_packages(packages):
    if not packages:
        secho("\nNo packages to install.", fg=GREEN)
        return

    secho(f"\nWill install packages: {packages}", fg=GREEN)

    cmd = f"apt-get install -qq -y {' '.join(packages)}"
    shell(cmd)


def install_nodejs(version="14.x"):
    # TODO: don't use curl (?)
    cmd = f"curl -sL https://deb.nodesource.com/setup_{version} | bash -"
    shell(cmd)

    shell("apt-get install -qq -y nodejs")
    shell("/usr/bin/npm install -g yarn")


def clear_apt_cache():
    shell("apt-get clean")
    shell("rm -rf /var/lib/apt/lists/*")
