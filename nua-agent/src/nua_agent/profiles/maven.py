from .. import sh
from .base import BaseProfile
from .common import check_requirements


class MavenProfile(BaseProfile):
    """Build a Java application using Maven."""

    label = "Java / Maven"

    builder_packages = [
        "maven",
    ]

    def accept(self):
        return self._check_files(["pom.xml"])

    def check(self):
        return check_requirements(["java", "mvn"])

    def build(self):
        sh.shell("mvn package")

    # def _build(self):
    #     java_path = join(ENV_ROOT, self.app)
    #     target_path = join(APP_ROOT, self.app, "target")
    #     env_file = join(APP_ROOT, self.app, "ENV")
    #     env = {
    #         "VIRTUAL_ENV": java_path,
    #         "PATH": ":".join(
    #             [join(java_path, "bin"), join(self.app, ".bin"), environ["PATH"]]
    #         ),
    #     }
    #     if exists(env_file):
    #         env.update(parse_settings(env_file, env))
    #     if not exists(java_path):
    #         makedirs(java_path)
    #     if not exists(target_path):
    #         echo("-----> Building Java Application")
    #         call("mvn package", cwd=join(APP_ROOT, self.app), env=env, shell=True)
    #
    #     else:
    #         echo("-----> Removing previous builds")
    #         echo("-----> Rebuilding Java Application")
    #         call("mvn clean package", cwd=join(APP_ROOT, self.app), env=env, shell=True)
