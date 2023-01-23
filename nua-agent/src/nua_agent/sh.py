import os
import shutil
from os import makedirs, mkdir
from shutil import copy as cp

__all__ = ["mkdir", "makedirs", "cp", "shell", "rm"]


def shell(cmd):
    print(cmd)
    status = os.system(cmd)
    if status != 0:
        raise RuntimeError("Command failed: " + cmd)


def rm(path: str, recursive: bool = False):
    if recursive:
        shutil.rmtree(path)
    else:
        os.unlink(path)
