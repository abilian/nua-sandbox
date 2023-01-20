from .. import sh
from .base import BaseProfile


class PhpProfile(BaseProfile):
    """Build a PHP application."""

    label = "PHP / Composer"

    def accept(self):
        return self._check_files(["composer.json"])

    def build(self):
        sh.shell("composer install")
