from .base import Builder
from .common import found_app
from .. import sh


class RustBuilder(Builder):
    """Build a Rust application."""

    builder_packages = [
        "rust-all",
    ]

    def accept(self):
        if self._check_files(["cargo.toml"]):
            found_app("Rust")
            return True
        return False

    def build(self):
        sh.shell("cargo build --release")
