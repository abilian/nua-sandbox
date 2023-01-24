import os

from .sh import shell

os.environ["DEBIAN_FRONTEND"] = "noninteractive"

# Not used. Remove soon.
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


# TODO: move this to the base image(s) so that it takes effect earlier.
# def configure_apt():
#     def echo(text: str, filename: str) -> None:
#         with open(filename, "w") as fd:
#             fd.write(text)
#
#     echo(
#         "Acquire::http {No-Cache=True;};",
#         "/etc/apt/apt.conf.d/no-cache",
#     )
#     echo(
#         'APT::Install-Recommends "0"; APT::Install-Suggests "0";',
#         "/etc/apt/apt.conf.d/01norecommend",
#     )
#     echo(
#         'Dir::Cache { srcpkgcache ""; pkgcache ""; }',
#         "/etc/apt/apt.conf.d/02nocache",
#     )
#     echo(
#         'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";',
#         "/etc/apt/apt.conf.d/02compress-indexes",
#     )


def install_packages(packages):
    if not packages:
        print()
        print("No packages to install.")
        print()
        return

    print()
    print("Will install packages: ", packages)
    print()

    cmd = "apt-get update -q"
    shell(cmd)

    # '--no-install-recommends' probably not needed.
    cmd = f"apt-get install -y --no-install-recommends {' '.join(packages)}"
    shell(cmd)


def install_nodejs(version="14.x"):
    # TODO: don't use curl (?)
    cmd = f"curl -sL https://deb.nodesource.com/setup_{version} | bash -"
    shell(cmd)

    shell("apt-get install -y nodejs")
    shell("/usr/bin/npm install -g yarn")


def clear_apt_cache():
    shell("apt-get clean")
    shell("rm -rf /var/lib/apt/lists/*")
