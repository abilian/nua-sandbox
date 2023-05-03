import tempfile
from pathlib import Path
from typing import cast
from urllib.error import HTTPError
from urllib.request import urlretrieve

from . import system
from .config import Config, read_config
from .profiles import PROFILE_CLASSES, BaseProfile
from .types import JsonDict
from .unarchiver import unarchive
from .utils import sh
from .utils.exceptions import Fail
from .utils.sh import virtualenv


class Builder:
    """Builds an app."""

    config: Config
    _profile: BaseProfile | None = None

    builder_packages: list[str] = []

    def __init__(self, config: JsonDict | None = None):
        if config:
            self.config = Config(config)
        else:
            self.config = read_config()

    @property
    def profile(self) -> BaseProfile:
        # Warning: profile detection can only happen after the source code has been fetched.
        return self._get_profile()

    #
    # Lifecycle methods (called from CLI i.e. `main.py`)
    #
    def fetch_app_source(self, strip_components=1):
        # Silence vulture while we figure out how to deal with this
        assert strip_components == 1

        # TODO: rewrite in pure Python and deal with all the cases (zip, git...)
        # Cf. download_extract() in nua/lib/actions.py
        src_url = self.config.get_str("metadata.src-url")
        print(f"Fetching: {src_url}")

        # shell(f"curl -sL {src_url} | tar xz --strip-components={strip_components} -f -")

        with tempfile.TemporaryDirectory() as tmp:
            if src_url:
                self.download_src(src_url, tmp)
                archive = Path(tmp) / Path(src_url).name
                unarchive(archive, ".")
            else:
                sh.shell("pwd")
                sh.shell("ls /nua")
                sh.shell("cp -r /nua/src/* .")

    def prepare(self):
        system.install_packages(self._get_system_packages())
        self.profile.prepare()

    def build_app(self):
        build_config = self.config.get("build", {})

        if "before-build" in build_config:
            sh.shell(build_config["before-build"])

        if Path("build.sh").exists():
            sh.shell("bash build.sh")
        else:
            self.profile.build()

        self._run_tests(build_config)

    def _run_tests(self, build_config: JsonDict):
        test = build_config.get("test")
        if not test:
            return

        print("Running smoke test(s)...")
        match cast(str | list[str], build_config["test"]):
            case str(line):
                test_lines = [line]
            case [*lines]:
                test_lines = lines
            case _:
                raise ValueError(f"Invalid test: {test}")

        with virtualenv("/nua/venv"):
            for test_line in test_lines:
                try:
                    sh.shell(test_line)
                except RuntimeError:
                    print(f"Test {test_line} failed.")
                    raise Fail(f"Test {test_line} failed.")

    def cleanup(self):
        self.profile.cleanup()

    #
    # Helpers methods
    #
    def download_src(self, url: str, tmp: str) -> None:
        name = Path(url).name
        # # FIXME: this decision should be delegated to the unarchivers
        # if not any(name.endswith(suf) for suf in (".zip", ".tar", ".tar.gz", ".tgz")):
        #     raise ValueError(f"Unknown archive format for '{name}'")
        target = Path(tmp) / name
        try:
            urlretrieve(url, target)
        except HTTPError as e:
            Fail(f"Error while downloading {url}: {e}")

    def _get_system_packages(self) -> list[str]:
        return self.profile.get_system_packages()

    def _get_profile(self) -> BaseProfile:
        build_config = self.config.get_dict("build")
        if builder_name := cast(str, build_config.get("builder", "")):
            if "-" in builder_name:
                builder_name = builder_name.split("-")[0]
            return self._get_builder(builder_name)
        return self._detect_profile()

    def _detect_profile(self) -> BaseProfile:
        for profile_cls in PROFILE_CLASSES:
            profile = profile_cls(self.config)
            if profile.accept():
                kind = profile_cls.label
                print(f"-----> {kind} app detected.")
                return profile

        raise Fail("No profile accepts to build this app.")

    def _get_builder(self, builder_name: str) -> BaseProfile:
        for profile_cls in PROFILE_CLASSES:
            if profile_cls.name == builder_name:
                return profile_cls(self.config)

        raise Fail(f"Unknown builder: {builder_name}")
