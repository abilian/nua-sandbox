import os
import re
import tarfile
import tempfile
from pathlib import Path
from urllib.request import urlopen, urlretrieve

import click
import typer

from . import sh, system
from .config import read_config
from .profiles import PROFILE_CLASSES, BaseProfile
from .sh import shell
from .types import JSON
from .unarchiver import unarchive


class Builder:
    """Builds an app."""

    config: JSON
    _profile: BaseProfile | None = None

    builder_packages: list[str] = []

    def __init__(self, config: JSON = None):
        if config:
            self.config = config
        else:
            self.config = read_config()

    @property
    def profile(self) -> BaseProfile:
        # Warning: profile detection can only happen after the source code has been fetched.
        return self._get_profile()

    def fetch_app_source(self, strip_components=1):
        # TODO: rewrite in pure Python and deal with all the cases (zip, git...)
        # Cf. download_extract() in nua/lib/actions.py
        metadata = self.config["metadata"]
        src_url = metadata["src-url"]
        print(f"Fetching: {src_url}")

        # shell(f"curl -sL {src_url} | tar xz --strip-components={strip_components} -f -")

        with tempfile.TemporaryDirectory() as tmp:
            self.download_src(src_url, tmp)
            archive = Path(tmp) / Path(src_url).name
            unarchive(archive, ".")

    def download_src(self, url: str, tmp: str) -> None:
        name = Path(url).name
        if not any(name.endswith(suf) for suf in (".zip", ".tar", ".tar.gz", ".tgz")):
            raise ValueError(f"Unknown archive format for '{name}'")
        target = Path(tmp) / name
        urlretrieve(url, target)

    def build(self):
        self.profile.build()

    def install_system_packages(self):
        system.install_packages(self._get_system_packages())
        self.profile.install_extra_packages()

    def _get_system_packages(self) -> list[str]:
        return self.profile.get_system_packages()

    def _get_profile(self) -> BaseProfile:
        if self._profile:
            return self._profile

        print("src content:")
        print([str(p) for p in Path(".").glob("*")])
        print()

        for profile_cls in PROFILE_CLASSES:
            profile = profile_cls(self.config)
            if profile.accept():
                kind = profile_cls.label
                click.secho(f"-----> {kind} app detected.", fg="green")
                return profile

        click.secho("No profile found.", fg="red")
        raise typer.Exit(1)
