from nua_agent.backports import chdir

from .. import sh
from .base import BaseProfile
from .common import check_requirements


class RubyProfile(BaseProfile):
    """Build a Ruby application using Bundler."""

    name = "ruby"
    label = "Ruby / Bundler"
    builder_packages = [
        "bundler",
        # "wget",
        # "pkg-config",
        # "build-essential",
        # "libpq-dev",
    ]

    def accept(self):
        return self._check_files(["Gemfile"])

    def check(self):
        return check_requirements(["ruby", "bundle"])

    def build(self):
        sh.shell("bundle install")

    # def install_ruby(self, version: str = "3.2.1"):
    #     """Installation of Ruby via 'ruby-install'.
    #
    #     Exec as root.
    #     """
    #     purge_package_list("ruby ruby-dev ri")
    #     options = "--disable-install-doc"
    #     if version.startswith("2.") or version.startswith("3.0"):
    #         ssl = compile_openssl_1_1()
    #         options = f"--disable-install-doc --with-openssl-dir={ssl}"
    #     ri_vers = "0.9.0"
    #
    #     with chdir("/tmp"):  # noqa s108
    #         cmd = (
    #             f"wget -O ruby-install-{ri_vers}.tar.gz "
    #             f"https://github.com/postmodern/ruby-install/archive/v{ri_vers}.tar.gz"
    #         )
    #         sh.shell(cmd)
    #         cmd = f"tar -xzvf ruby-install-{ri_vers}.tar.gz"
    #         sh.shell(cmd)
    #         with chdir(f"ruby-install-{ri_vers}"):
    #             cmd = "make install"
    #             sh.shell(cmd)
    #
    #     cmd = f"rm -fr /tmp/ruby-install-{ri_vers}*"
    #     sh.shell(cmd)

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
