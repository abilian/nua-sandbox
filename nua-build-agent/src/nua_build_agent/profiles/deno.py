import os

from ..utils.sh import environment, shell
from .base import BaseProfile


class DenoProfile(BaseProfile):
    """Build a Deno app."""

    name = "deno"
    label = "Deno"

    builder_packages = [
        "unzip",
    ]

    def accept(self):
        # No way to autodetect, one a
        return False

    def prepare(self):
        install_deno()

    def build(self):
        pass


def install_deno():
    with environment(DENO_INSTALL="/nua/deno"):
        cmd = "curl -fsSL https://deno.land/x/install/install.sh | sh"
        # Can't use subprocess here because of the pipe
        print(f"$ {cmd}")
        os.system(cmd)

        shell("mkdir -p /nua/bin")
        shell("ln -sf /nua/deno/bin/deno /nua/bin/deno")
        shell("/nua/bin/deno --version")
