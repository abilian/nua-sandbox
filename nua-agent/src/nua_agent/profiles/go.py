from pathlib import Path

from ..utils import sh
from .base import BaseProfile
from .common import check_requirements


class GoProfile(BaseProfile):
    """Build a Go application using Go."""

    name = "go"
    label = "Go"
    builder_packages = ["golang-go"]

    def accept(self):
        return Path("go.mod").exists()
        # Was:
        # return (
        #     (
        #         exists(join(self.app_path, "Godeps"))
        #         or len(glob(join(self.app_path, "*.go")))
        #     )
        #     and found_app("Go")
        # )

    def check(self):
        return check_requirements(["go"])

    def build(self):
        sh.shell("go get")
        sh.shell("go build -o out")

    # def _build(self):
    #     go_path = join(ENV_ROOT, self.app)
    #     deps = join(APP_ROOT, self.app, "Godeps")
    #     first_time = False
    #
    #     if not exists(go_path):
    #         echo(f"-----> Creating GOPATH for '{self.app}'", fg="green")
    #         makedirs(go_path)
    #         # copy across a pre-built GOPATH to save provisioning time
    #         call(f"cp -a $HOME/gopath {self.app}", cwd=ENV_ROOT, shell=True)
    #         first_time = True
    #
    #     if exists(deps):
    #         if first_time or getmtime(deps) > getmtime(go_path):
    #             echo(f"-----> Running godep for '{self.app}'", fg="green")
    #             env = {
    #                 "GOPATH": "$HOME/gopath",
    #                 "GOROOT": "$HOME/go",
    #                 "PATH": "$PATH:$HOME/go/bin",
    #                 "GO15VENDOREXPERIMENT": "1",
    #             }
    #             call(
    #                 "godep update ...",
    #                 cwd=join(APP_ROOT, self.app),
    #                 env=env,
    #                 shell=True,
    #             )
