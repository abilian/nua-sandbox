import os
import shlex
import shutil
import subprocess
import sys
from contextlib import contextmanager
from os import makedirs, mkdir
from pathlib import Path
from shutil import copy as cp

__all__ = ["mkdir", "makedirs", "cp", "shell", "rm"]


def shell(cmd):
    print(cmd)
    sys.stdout.flush()

    args = shlex.split(cmd)
    subprocess.check_call(args)


def rm(path: str, recursive: bool = False):
    if recursive:
        shutil.rmtree(path)
    else:
        os.unlink(path)


@contextmanager
def virtualenv(path: str | Path):
    """Create a virtualenv and activate it."""
    env = os.environ.copy()
    os.environ["PATH"] = f"{path}/bin:" + env["PATH"]
    yield
    os.environ = env  # type: ignore
