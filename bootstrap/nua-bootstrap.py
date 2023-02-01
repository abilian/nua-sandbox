from pyinfra.operations import server, files, apt, pip, systemd, git

USER = "nua"
GROUP = "nua"
NUA_HOME = f"/home/{USER}"
NUA_GIT_URL = "https://github.com/abilian/nua.git"
FOLDERS = (
    ".",
    "tmp",
    "log",
    "db",
    "config",
    "apps",
    "images",
    "git",
    "backups",
)
VENV = f"{NUA_HOME}/venv"
HOST_PACKAGES = [
    "ca-certificates",
    "curl",
    "docker.io",
    "lsb-release",
    "git",
    "nginx-light",
    "software-properties-common",
    "python3-certbot-nginx",
]
PYTHON_PACKAGES = [
    "pip",
    "setuptools",
    "wheel",
    # "poetry",
]
NGINX_FOLDERS = (
    "conf.d",
    "sites",
)


def ctx():
    d = {}
    for k, v in globals().items():
        if k.isupper():
            d[k] = v
    return d


def bootstrap():
    install_host_packages()
    create_nua_user()
    setup_nua_venv()
    setup_nginx()
    install_orchestrator()

    # bootstrap_install_postgres_or_fail()
    # bootstrap_install_mariadb_or_fail()
    # install_local_orchestrator()
    # create_nua_key()
    # create_ssl_key()


def install_host_packages():
    apt.packages(
        HOST_PACKAGES,
        update=True,
        no_recommends=True,
    )


def create_nua_user():
    server.user(
        name="Create nua user",
        user=USER,
        group="docker",
        home=NUA_HOME,
    )
    for folder in FOLDERS:
        path = f"{NUA_HOME}/{folder}"
        files.directory(
            name=f"Create folder {path}",
            path=path,
            user=USER,
            group=GROUP,
            mode="755",
        )


def setup_nua_venv():
    pip.venv(
        name="Create a virtualenv",
        path=VENV,
        python="python3",
        _su_user=USER,
    )
    pip.packages(
        name="Install python packages",
        packages=PYTHON_PACKAGES,
        virtualenv=VENV,
        _su_user=USER,
    )


def setup_nginx():
    path = f"{NUA_HOME}/nginx"
    files.directory(
        name=f"Create folder: {path}",
        path=path,
        user=USER,
        group=GROUP,
        mode="755",
    )
    for folder in NGINX_FOLDERS:
        path = f"{NUA_HOME}/nginx/{folder}"
        files.directory(
            name=f"Create folder: {path}",
            path=path,
            user=USER,
            group=GROUP,
            mode="755",
        )

    files.template(
        name="Replace nginx config file",
        src="templates/nginx.conf.j2",
        dest="/etc/nginx/nginx.conf",
        **ctx(),
    )
    files.template(
        name="Replace nginx default site config file",
        src="templates/default-site.conf.j2",
        dest=f"{NUA_HOME}/nginx/sites/00default.conf",
        user=USER,
        group=GROUP,
        **ctx(),
    )
    files.sync(
        name="Sync default assets",
        src="templates/www/assets",
        dest=f"{NUA_HOME}/nginx/www/assets",
        delete=True,
        user="www-data",
        group="www-data",
    )
    files.template(
        name="Push default index.html",
        src="templates/www/index.html.j2",
        dest=f"{NUA_HOME}/nginx/www/index.html",
        user=USER,
        group=GROUP,
        **ctx(),
    )

    systemd.service(
        name="Restart nginx",
        service="nginx",
        enabled=True,
        restarted=True,
        reloaded=True,
    )


def install_orchestrator():
    git.repo(
        name="Clone Nua source code",
        src=NUA_GIT_URL,
        dest=f"{NUA_HOME}/git/nua",
        branch="main",
    )

    pip.packages(
        name="Install nua-orchestrator & dependencies",
        packages=[f"{NUA_HOME}/git/nua/nua-lib", f"{NUA_HOME}/git/nua/nua-orchestrator"],
        virtualenv=VENV,
    )

    server.shell(
        name="Check nua-orchestrator installation",
        commands=[f"{VENV}/bin/nua-orchestrator status"],
    )



bootstrap()
