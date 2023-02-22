from .. import sh
from .base import BaseProfile
from .common import check_requirements


class RustProfile(BaseProfile):
    """Build a Rust application."""

    name = "rust"
    label = "Rust / Cargo"
    builder_packages = [
        "rust-all",
    ]

    def accept(self):
        return self._check_files(["Cargo.toml"])

    def check(self):
        return check_requirements(["cargo"])

    def build(self):
        sh.shell("cargo build --release")
