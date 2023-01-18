import os

from .config import read_config
from .sh import shell

os.environ["DEBIAN_FRONTEND"] = "noninteractive"

PACKAGES = [
    # Stuff
    "apt-utils",
    # Web stuff
    "ca-certificates",
    "curl",
    # Build stuff
    "software-properties-common",
    "build-essential",
    "make",
    "gcc",
    "g++",
    "git",
]


def configure_apt():
    echo(
        "Acquire::http {No-Cache=True;};",
        "/etc/apt/apt.conf.d/no-cache",
    )
    echo(
        'APT::Install-Recommends "0"; APT::Install-Suggests "0";',
        "/etc/apt/apt.conf.d/01norecommend",
    )
    echo(
        'Dir::Cache { srcpkgcache ""; pkgcache ""; }',
        "/etc/apt/apt.conf.d/02nocache",
    )
    echo(
        'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";',
        "/etc/apt/apt.conf.d/02compress-indexes",
    )


def install_packages(packages):
    print()
    print("Will install packages: ", packages)
    print()

    cmd = f"apt-get update -q"
    shell(cmd)

    cmd = f"apt-get install -y {' '.join(packages)}"
    shell(cmd)


def install_nodejs():
    cmd = "curl -sL https://deb.nodesource.com/setup_18.x | bash -"
    shell(cmd)

    shell("apt-get install -y nodejs")
    shell("/usr/bin/npm install -g yarn")


def clear_apt_cache():
    shell("apt-get clean")
    shell("rm -rf /var/lib/apt/lists/*")


def echo(text: str, filename: str) -> None:
    with open(filename, "w") as fd:
        fd.write(text)
