import os

from .. import sh
from .base import BaseProfile

# TODO: we should probably install the app in a virtualenv.


class PythonProfile(BaseProfile):
    """Build a Python application."""

    label = "Python / Pip"

    def accept(self):
        return self._check_files(["setup.py", "requirements.txt", "pyproject.toml"])

    def build(self):
        if self._check_files(["requirements.txt"]):
            sh.shell("pip install -r requirements.txt")
        else:
            sh.shell("pip install .")

    # def _build(self):
    #     virtualenv_path = join(ENV_ROOT, self.app_id)
    #     requirements = join(APP_ROOT, self.app_id, "requirements.txt")
    #     env_file = join(APP_ROOT, self.app_id, "ENV")
    #     # Peek at environment variables shipped with repo (if any) to determine version
    #     env = {}
    #     if exists(env_file):
    #         env.update(parse_settings(env_file, env))
    #
    #     # TODO: improve version parsing
    #     # pylint: disable=unused-variable
    #     version = int(env.get("PYTHON_VERSION", "3"))
    #     first_time = False
    #     if not exists(join(virtualenv_path, "bin", "activate")):
    #         echo(f"-----> Creating virtualenv for '{self.app_id}'", fg="green")
    #         try:
    #             makedirs(virtualenv_path)
    #         except FileExistsError:
    #             echo(f"-----> Env dir already exists: '{self.app_id}'", fg="yellow")
    #         call(
    #             f"virtualenv --python=python{version:d} {self.app_id:s}",
    #             cwd=ENV_ROOT,
    #             shell=True,
    #         )
    #         first_time = True
    #     activation_script = join(virtualenv_path, "bin", "activate_this.py")
    #     exec(open(activation_script).read(), dict(__file__=activation_script))
    #     if first_time or getmtime(requirements) > getmtime(virtualenv_path):
    #         echo(f"-----> Running pip for '{self.app_id}'", fg="green")
    #         call(f"pip install -r {requirements}", cwd=virtualenv_path, shell=True)
