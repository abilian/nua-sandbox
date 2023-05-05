from ..utils import sh
from .base import BaseProfile
from .common import check_requirements


class ClojureProfile(BaseProfile):
    """Build a Clojure application using Leiningen."""

    name = "clojure"
    label = "Clojure / Lein"

    builder_packages = [
        "leiningen",
    ]

    def accept(self):
        return self._check_files(["project.clj"])

    def check(self):
        return check_requirements(["java", "lein"])

    def build(self):
        sh.shell("lein uberjar")

    # def _build(self):
    #     virtual = join(ENV_ROOT, self.app)
    #     target_path = join(APP_ROOT, self.app, "target")
    #     env_file = join(APP_ROOT, self.app, "ENV")
    #     if not exists(target_path):
    #         makedirs(virtual)
    #     env = {
    #         "VIRTUAL_ENV": virtual,
    #         "PATH": ":".join(
    #             [join(virtual, "bin"), join(self.app, ".bin"), environ["PATH"]]
    #         ),
    #         "LEIN_HOME": environ.get("LEIN_HOME", join(environ["HOME"], ".lein")),
    #     }
    #     if exists(env_file):
    #         env.update(parse_settings(env_file, env))
    #     echo("-----> Building Clojure Application")
    #     call("lein clean", cwd=join(APP_ROOT, self.app), env=env, shell=True)
    #     call("lein uberjar", cwd=join(APP_ROOT, self.app), env=env, shell=True)
