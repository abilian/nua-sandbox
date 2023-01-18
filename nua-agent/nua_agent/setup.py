import os

from nua_agent.sh import system

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


def main():
    configure_apt()
    install_packages()
    install_nodejs()


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


def install_packages():
    cmd = f"apt-get update"
    system(cmd)

    cmd = f"apt-get install -y {' '.join(PACKAGES)}"
    system(cmd)


def install_nodejs():
    cmd = "curl -sL https://deb.nodesource.com/setup_18.x | bash -"
    system(cmd)

    system("apt-get install -y nodejs")
    system("/usr/bin/npm install -g yarn")


def echo(text: str, filename: str) -> None:
    with open(filename, "w") as fd:
        fd.write(text)
