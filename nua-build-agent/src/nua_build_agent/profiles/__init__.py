from nua_build_agent.profiles.deno import DenoProfile

from .base import BaseProfile
from .clojure import ClojureProfile
from .go import GoProfile
from .gradle import GradleProfile
from .maven import MavenProfile
from .node import NodeProfile
from .php import PhpProfile
from .python import PythonProfile
from .ruby import RubyProfile
from .rust import RustProfile

PROFILE_CLASSES: list[type[BaseProfile]] = [
    PythonProfile,
    RubyProfile,
    NodeProfile,
    PhpProfile,
    MavenProfile,
    GradleProfile,
    GoProfile,
    ClojureProfile,
    RustProfile,
    DenoProfile,
]


# def do_deploy(app, deltas=None, newrev=None):
#     """Deploy an app by resetting the work directory."""
#
#     deltas = deltas or {}
#
#     app_path = join(APP_ROOT, app)
#     procfile = join(app_path, "Procfile")
#     log_path = join(LOG_ROOT, app)
#
#     env = {"GIT_WORK_DIR": app_path}
#     if not exists(app_path):
#         echo(f"Error: app '{app}' not found.", fg="red")
#         # TODO: raise exception ?
#         return
#
#     echo(f"-----> Deploying app '{app}'", fg="green")
#
#     call("git fetch --quiet", cwd=app_path, env=env, shell=True)
#     if newrev:
#         call(f"git reset --hard {newrev}", cwd=app_path, env=env, shell=True)
#     call("git submodule init", cwd=app_path, env=env, shell=True)
#     call("git submodule update", cwd=app_path, env=env, shell=True)
#     if not exists(log_path):
#         makedirs(log_path)
#
#     workers = parse_procfile(procfile)
#     if not workers or len(workers) <= 0:
#         echo(f"Error: Invalid Procfile for app '{app}'.", fg="red")
#         # TODO: raise exception ?
#         return
#
#     settings = {}
#
#     for builder_class in BUILDER_CLASSES:
#         deployer = builder_class(app=app)
#         if deployer.accept():
#             settings.update(deployer.deploy(deltas))
#
#         # TODO: refactor this too
#         else:
#             if "release" in workers and "web" in workers:
#                 echo("-----> Generic app detected.", fg="green")
#                 settings.update(deploy_identity(app, deltas))
#             elif "static" in workers:
#                 echo("-----> Static app detected.", fg="green")
#                 settings.update(deploy_identity(app, deltas))
#             else:
#                 echo("-----> Could not detect runtime!", fg="red")
#
#     # TODO: detect other runtimes
#     if "release" in workers:
#         echo("-----> Releasing", fg="green")
#         retval = call(workers["release"], cwd=app_path, env=settings, shell=True)
#         if retval:
#             echo(f"-----> Exiting due to release command error value: {retval}")
#             exit(retval)
#         workers.pop("release", None)
#
#
# def deploy_identity(app, deltas=None):
#     deltas = deltas or {}
#
#     env_path = join(ENV_ROOT, app)
#     if not exists(env_path):
#         makedirs(env_path)
#
#     return spawn_app(app, deltas)
