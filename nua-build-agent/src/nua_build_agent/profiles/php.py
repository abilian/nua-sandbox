from subprocess import CalledProcessError

from ..utils import sh
from .base import BaseProfile


class PhpProfile(BaseProfile):
    """Build a PHP application (using Composer)."""

    name = "php"
    label = "PHP / Composer"
    builder_packages = [
        "build-essential",
        # NB: Probably not needed at runtime
        "composer",
        # Useful for composer install
        "php-curl",
        # Maybe not useful at runtime (or app-specific)
        "php-xml",
    ]

    def accept(self):
        return self._check_files(["composer.json"])

    def build(self):
        try:
            sh.shell("composer install")
        except CalledProcessError:
            # FIXME: if this happens, the upstream package is probably broken.
            sh.shell("composer update")
            sh.shell("composer install")
