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
from .utils.backports import chdir
from .utils.exceptions import Fail
from .utils.sh import cp, virtualenv


#
# TODO:
# - Rename it: call it Agent, not Builder (and rename "Profiles" to "Builders") ?
# - Introduce "AgentStage" classes ?
#
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
        """Fetches the app source code (if needed) and puts it in
        /nua/build/src/."""
        # Silence vulture while we figure out how to deal with this
        assert strip_components == 1

        src_url = self.config.get_str("metadata.src-url")

        # Was:
        # shell(f"curl -sL {src_url} | tar xz --strip-components={strip_components} -f -")

        # TODO: rewrite in pure Python and deal with all the cases (zip, git...)
        # Cf. download_extract() in nua/lib/actions.py
        if src_url:
            print(f"Fetching: {src_url}")
            with tempfile.TemporaryDirectory() as tmp:
                self.download_src(src_url, tmp)
                archive = Path(tmp) / Path(src_url).name
                print(f"Unarchiving {archive} to /nua/build/src/")
                unarchive(archive, "/nua/build/src")
        else:
            print("No source URL, skipping fetch.")

        assert len(list(Path("/nua/build/src").glob("*"))) > 0

    def prepare(self):
        """Prepare the build environment (install packages, etc.).

        To be replaced by something more fine-grained.
        """
        system.install_packages(self._get_system_packages())
        self.profile.prepare()

    def build_app(self):
        """Build the app."""
        if before_build := self.config.get(["build", "before-build"]):
            sh.shell(before_build)

        with chdir("/nua/build/src"):
            if build_command := self.config.get(["build", "build-command"]):
                if isinstance(build_command, str):
                    build_commands = [build_command]
                else:
                    build_commands = build_command
                for command in build_commands:
                    sh.shell(command)

            # FIXME: remove or make it clean there is a convention
            elif Path("build.sh").exists():
                sh.shell("bash build.sh")

            else:
                # Use the generic build method of the builder
                self.profile.build()

            self._run_tests()

    def _run_tests(self):
        test_cmd = self.config.get(["build", "test"])
        if not test_cmd:
            return

        print("Running smoke test(s)...")
        match cast(str | list[str], test_cmd):
            case str(line):
                test_lines = [line]
            case [*lines]:
                test_lines = lines
            case _:
                raise ValueError(f"Invalid test: {test_cmd}")

        with virtualenv("/nua/venv"):
            for test_line in test_lines:
                try:
                    sh.shell(test_line)
                except RuntimeError:
                    print(f"Test {test_line} failed.")
                    raise Fail(f"Test {test_line} failed.")

    def install(self):
        """Install the app."""
        Path("/nua/metadata").mkdir(exist_ok=True)
        Path("/nua/app").mkdir(exist_ok=True)
        # FIXME: _nua-config.json will probably move someplace else
        cp("/nua/build/_nua-config.json", "/nua/metadata/nua-config.json")

    def check(self):
        """Install the app."""
        assert Path("/nua/metadata/nua-config.json").exists()
        assert Path("/nua/app").exists()
        # TODO:
        # assert not Path("/nua/build").exists()

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
        with chdir("/nua/build/src"):
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
