# TODO: duplicate code...

import os
import shutil

__all__ = ["shell", "cp"]


def shell(cmd):
    # TODO: better use subprocess
    print(cmd)
    status = os.system(cmd)
    if status != 0:
        raise RuntimeError(f"Command failed: {cmd!r}")


def cp(src, dst):
    shutil.copy(src, dst)
