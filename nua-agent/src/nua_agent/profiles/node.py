from .. import sh
from ..system import install_nodejs
from .base import BaseProfile
from .common import check_requirements


class NodeProfile(BaseProfile):
    """Build a Noejs app."""

    name = "node"
    label = "Node.js / NPM or Yarn"
    builder_packages = [
        "git",
    ]

    def accept(self):
        return self._check_files(["package.json"])

    def check(self) -> bool:
        return (
            check_requirements(["nodejs", "npm"])
            or check_requirements(["node", "npm"])
            or check_requirements(["nodeenv"])
        )

    def prepare(self):
        build_config = self.config.get("build", {})
        node_version = build_config.get("node-version", "14.x")
        install_nodejs(node_version)
        sh.shell("ln -sf /usr/bin/yarnpkg /usr/bin/yarn")

    def build(self):
        print("yarn version:")
        sh.shell("yarn --version")
        print("npm version:")
        sh.shell("npm --version")

        if self._check_files(["package-lock.json"]):
            sh.shell("npm install")
        elif self._check_files(["yarn.lock"]):
            sh.shell("yarn install --production=true --pure-lockfile")
        else:
            sh.shell("npm install")

        # virtual = join(ENV_ROOT, self.app)
        # virtualenv_path = join(ENV_ROOT, self.app)
        # node_path = join(ENV_ROOT, self.app, "node_modules")
        # node_modules_symlink = join(APP_ROOT, self.app, "node_modules")
        # npm_prefix = abspath(join(node_path, ".."))
        # env_file = join(APP_ROOT, self.app, "ENV")
        # deps = join(APP_ROOT, self.app, "package.json")
        # first_time = False
        # if not exists(node_path):
        #     echo(f"-----> Creating node_modules for '{self.app}'", fg="green")
        #     makedirs(node_path)
        #     first_time = True
        # env = {
        #     "VIRTUAL_ENV": virtualenv_path,
        #     "NODE_PATH": node_path,
        #     "NPM_CONFIG_PREFIX": npm_prefix,
        #     "PATH": ":".join(
        #         [join(virtualenv_path, "bin"), join(node_path, ".bin"), environ["PATH"]]
        #     ),
        # }
        # if exists(env_file):
        #     env.update(parse_settings(env_file, env))
        #
        # # include node binaries on our path
        # environ["PATH"] = env["PATH"]
        # version = env.get("NODE_VERSION")
        # node_binary = join(virtualenv_path, "bin", "node")
        # installed = (
        #     check_output(
        #         f"{node_binary} -v", cwd=join(APP_ROOT, self.app), env=env, shell=True
        #     )
        #     .decode("utf8")
        #     .rstrip("\n")
        #     if exists(node_binary)
        #     else ""
        # )
        # if version and check_requirements(["nodeenv"]):
        #     if not installed.endswith(version):
        #         started = glob(join(UWSGI_ENABLED, f"{self.app}*.ini"))
        #         if installed and len(started):
        #             echo(
        #                 "Warning: Can't update node with app running. Stop the app & retry.",
        #                 fg="yellow",
        #             )
        #         else:
        #             echo(
        #                 "-----> Installing node version '{NODE_VERSION:s}' using nodeenv".format(
        #                     **env
        #                 ),
        #                 fg="green",
        #             )
        #             call(
        #                 "nodeenv --prebuilt --node={NODE_VERSION:s} --clean-src --force {VIRTUAL_ENV:s}".format(
        #                     **env
        #                 ),
        #                 cwd=virtualenv_path,
        #                 env=env,
        #                 shell=True,
        #             )
        #     else:
        #         echo(f"-----> Node is installed at {version}.")
        #
        # if exists(deps) and check_requirements(["npm"]):
        #     if first_time or getmtime(deps) > getmtime(node_path):
        #         copyfile(
        #             join(APP_ROOT, self.app, "package.json"),
        #             join(ENV_ROOT, self.app, "package.json"),
        #         )
        #         if not exists(node_modules_symlink):
        #             symlink(node_path, node_modules_symlink)
        #         echo(f"-----> Running npm for '{self.app}'", fg="green")
        #         call(
        #             f"npm install --prefix {npm_prefix} --package-lock=false",
        #             cwd=join(APP_ROOT, self.app),
        #             env=env,
        #             shell=True,
        #         )
