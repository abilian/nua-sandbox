"""System utilities."""
import os

from cleez.colors import blue, green

from .utils.sh import shell

os.environ["DEBIAN_FRONTEND"] = "noninteractive"


def install_packages(packages):
    if not packages:
        print(green("\nNo packages to install."))
        return

    print(blue(f"\nWill install packages: {packages}"))

    cmd = f"apt-get install -qq -y {' '.join(packages)}"
    shell(cmd)


def clear_apt_cache():
    shell("apt-get clean")
    shell("rm -rf /var/lib/apt/lists")
