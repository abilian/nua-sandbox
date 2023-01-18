from os import environ, makedirs
from os.path import exists, join
from subprocess import call

from click import secho as echo

from .base import Builder
from .common import check_requirements, found_app


class MavenBuilder(Builder):
    """Build a Java application using Maven."""

    def accept(self):
        if not self._check_files(["pom.xml"]):
            return False
        found_app("Java Maven")
        return check_requirements(["java", "mvn"])

    def _build(self):
        java_path = join(ENV_ROOT, self.app)
        target_path = join(APP_ROOT, self.app, "target")
        env_file = join(APP_ROOT, self.app, "ENV")
        env = {
            "VIRTUAL_ENV": java_path,
            "PATH": ":".join(
                [join(java_path, "bin"), join(self.app, ".bin"), environ["PATH"]]
            ),
        }
        if exists(env_file):
            env.update(parse_settings(env_file, env))
        if not exists(java_path):
            makedirs(java_path)
        if not exists(target_path):
            echo("-----> Building Java Application")
            call("mvn package", cwd=join(APP_ROOT, self.app), env=env, shell=True)

        else:
            echo("-----> Removing previous builds")
            echo("-----> Rebuilding Java Application")
            call("mvn clean package", cwd=join(APP_ROOT, self.app), env=env, shell=True)
