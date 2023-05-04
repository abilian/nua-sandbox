"""System utilities."""
import os

from cleez.colors import blue, green

from .utils.sh import environment, shell

os.environ["DEBIAN_FRONTEND"] = "noninteractive"


def install_packages(packages):
    if not packages:
        print(green("\nNo packages to install."))
        return

    print(blue(f"\nWill install packages: {packages}"))

    cmd = f"apt-get install -qq -y {' '.join(packages)}"
    shell(cmd)


def install_nodejs(version="14.x"):
    # TODO: don't use curl (?)
    cmd = f"curl -sL https://deb.nodesource.com/setup_{version} | bash -"
    # Can't use subprocess here because of the pipe
    print(f"$ {cmd}")
    os.system(cmd)

    shell("apt-get install -qq -y nodejs")
    shell("/usr/bin/npm install -g yarn")


def install_deno():
    with environment(DENO_INSTALL="/nua/deno"):
        cmd = "curl -fsSL https://deno.land/x/install/install.sh | sh"
        # Can't use subprocess here because of the pipe
        print(f"$ {cmd}")
        os.system(cmd)

        shell("mkdir -p /nua/bin")
        shell("ln -sf /nua/deno/bin/deno /nua/bin/deno")
        shell("/nua/bin/deno --version")


def clear_apt_cache():
    shell("apt-get clean")
    shell("rm -rf /var/lib/apt/lists")
