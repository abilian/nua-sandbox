from .. import sh
from .base import BaseProfile
from .common import check_requirements


class RubyProfile(BaseProfile):
    """Build a Ruby application using Bundler."""

    name = "ruby"
    label = "Ruby / Bundler"
    builder_packages = [
        "bundler",
    ]

    def accept(self):
        return self._check_files(["Gemfile"])

    def check(self):
        return check_requirements(["ruby", "bundle"])

    def build(self):
        sh.shell("bundle install")

    # def _build(self):
    #     virtual = join(ENV_ROOT, self.app)
    #     env_file = join(APP_ROOT, self.app, "ENV")
    #     env = {
    #         "VIRTUAL_ENV": virtual,
    #         "PATH": ":".join(
    #             [join(virtual, "bin"), join(self.app, ".bin"), environ["PATH"]]
    #         ),
    #     }
    #
    #     if exists(env_file):
    #         env.update(parse_settings(env_file, env))
    #
    #     if not exists(virtual):
    #         echo("-----> Building Ruby Application")
    #         makedirs(virtual)
    #     else:
    #         echo("------> Rebuilding Ruby Application")
    #
    #     call("bundle install", cwd=join(APP_ROOT, self.app), env=env, shell=True)
