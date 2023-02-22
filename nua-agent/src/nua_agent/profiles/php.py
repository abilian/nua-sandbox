from .. import sh
from .base import BaseProfile


class PhpProfile(BaseProfile):
    """Build a PHP application."""

    name = "php"
    label = "PHP / Composer"
    builder_packages = [
        "composer",
    ]

    def accept(self):
        return self._check_files(["composer.json"])

    def build(self):
        sh.shell("composer install")
