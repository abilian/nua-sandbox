"""Shell-like utilities."""

import os
import shlex
import shutil
import subprocess
import sys
from contextlib import contextmanager
from os import makedirs, mkdir
from pathlib import Path

__all__ = ["mkdir", "makedirs", "cp", "shell", "rm", "virtualenv"]


def shell(cmd):
    # HACK (fixme later)
    if "/nua/bin:" not in os.environ["PATH"]:
        os.environ["PATH"] = "/nua/bin:" + os.environ["PATH"]

    print(f"$ {cmd}")
    sys.stdout.flush()

    args = shlex.split(cmd)
    subprocess.check_call(args)


def rm(path: str, recursive: bool = False):
    if recursive:
        shutil.rmtree(path)
    else:
        os.unlink(path)


def cp(src, dst, recursive: bool = False):
    if recursive:
        shutil.copytree(src, dst)
    else:
        shutil.copy(src, dst)


@contextmanager
def virtualenv(path: str | Path):
    """Create a virtualenv and activate it."""
    env = os.environ.copy()
    os.environ["PATH"] = f"{path}/bin:" + env["PATH"]
    yield
    os.environ = env  # type: ignore


@contextmanager
def environment(**kw):
    """Run something with a modified environement."""
    env = os.environ.copy()
    for k, v in kw.items():
        os.environ[k] = str(v)
    yield
    os.environ = env  # type: ignore
