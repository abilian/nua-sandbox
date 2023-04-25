from nua_agent.system import install_deno

from .base import BaseProfile


class DenoProfile(BaseProfile):
    """Build a Deno app."""

    name = "deno"
    label = "Deno"

    builder_packages = [
        "unzip",
    ]

    def accept(self):
        # No way to autodetect
        return False

    def check(self) -> bool:
        return True

    def prepare(self):
        install_deno()

    def build(self):
        pass
