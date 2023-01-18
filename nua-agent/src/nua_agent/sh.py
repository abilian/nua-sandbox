import os
from os import makedirs, mkdir
from shutil import copy as cp

__all__ = ["mkdir", "makedirs", "cp", "shell"]


def shell(cmd):
    print(cmd)
    status = os.system(cmd)
    if status != 0:
        raise RuntimeError("Command failed: " + cmd)
