from os import environ, makedirs
from os.path import exists, join
from subprocess import call

from click import secho as echo

from .base import Builder
from .common import check_requirements, found_app


class RubyBuilder(Builder):
    """Build a Ruby application using Bundler."""

    def accept(self):
        if not self._check_files(["Gemfile"]):
            return False
        found_app("Ruby Application")
        return check_requirements(["ruby", "bundle"])

    def _build(self):
        virtual = join(ENV_ROOT, self.app)
        env_file = join(APP_ROOT, self.app, "ENV")
        env = {
            "VIRTUAL_ENV": virtual,
            "PATH": ":".join(
                [join(virtual, "bin"), join(self.app, ".bin"), environ["PATH"]]
            ),
        }

        if exists(env_file):
            env.update(parse_settings(env_file, env))

        if not exists(virtual):
            echo("-----> Building Ruby Application")
            makedirs(virtual)
        else:
            echo("------> Rebuilding Ruby Application")

        call("bundle install", cwd=join(APP_ROOT, self.app), env=env, shell=True)
