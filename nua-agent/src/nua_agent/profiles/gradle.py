from ..utils import sh
from .base import BaseProfile
from .common import check_requirements


class GradleProfile(BaseProfile):
    """Build a Java application using Gradle."""

    name = "gradle"
    label = "Java / Gradle"
    builder_packages = [
        "gradle",
    ]

    def accept(self):
        return self._check_files(["build.gradle"])

    def check(self):
        return check_requirements(["java", "gradle"])

    def build(self):
        sh.shell("gradle build")

    # def _build(self):
    #     java_path = join(ENV_ROOT, self.app)
    #     build_path = join(APP_ROOT, self.app, "build")
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
    #     if not exists(build_path):
    #         echo("-----> Building Java Application")
    #         call("gradle build", cwd=join(APP_ROOT, self.app), env=env, shell=True)
    #
    #     else:
    #         echo("-----> Removing previous builds")
    #         echo("-----> Rebuilding Java Application")
    #         call(
    #             "gradle clean build", cwd=join(APP_ROOT, self.app), env=env, shell=True
    #         )
