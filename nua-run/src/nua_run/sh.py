# TODO: duplicate code...

import os
from shutil import copy as cp

__all__ = ["shell", "cp"]


def shell(cmd):
    # TODO: better use subprocess
    print(cmd)
    status = os.system(cmd)
    if status != 0:
        raise RuntimeError(f"Command failed: {cmd!r}")
