import os
from os import mkdir, makedirs
from shutil import copy as cp

__all__ = ["mkdir", "makedirs", "cp", "shell"]


def shell(cmd):
    print(cmd)
    os.system(cmd)
