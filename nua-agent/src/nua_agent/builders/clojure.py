from os import environ, makedirs
from os.path import exists, join
from subprocess import call

from click import secho as echo

from .base import Builder
from .common import check_requirements, found_app


class ClojureBuilder(Builder):
    """Build a Clojure application using Leiningen."""

    def accept(self):
        if not self._check_files(["project.clj"]):
            return False
        found_app("Clojure Lein")
        return check_requirements(["java", "lein"])

    def _build(self):
        virtual = join(ENV_ROOT, self.app)
        target_path = join(APP_ROOT, self.app, "target")
        env_file = join(APP_ROOT, self.app, "ENV")
        if not exists(target_path):
            makedirs(virtual)
        env = {
            "VIRTUAL_ENV": virtual,
            "PATH": ":".join(
                [join(virtual, "bin"), join(self.app, ".bin"), environ["PATH"]]
            ),
            "LEIN_HOME": environ.get("LEIN_HOME", join(environ["HOME"], ".lein")),
        }
        if exists(env_file):
            env.update(parse_settings(env_file, env))
        echo("-----> Building Clojure Application")
        call("lein clean", cwd=join(APP_ROOT, self.app), env=env, shell=True)
        call("lein uberjar", cwd=join(APP_ROOT, self.app), env=env, shell=True)
