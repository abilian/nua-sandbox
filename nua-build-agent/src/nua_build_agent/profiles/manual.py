from .base import BaseProfile


class ManualProfile(BaseProfile):
    """Build an app with explicit commands."""

    name = "manual"
    label = "Manual"

    builder_packages = []

    def accept(self):
        # No way to autodetect
        return False

    def build(self):
        pass
