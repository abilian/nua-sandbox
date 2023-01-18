# TODO: duplicate code...

import os
from shutil import copy as cp

__all__ = ["shell", "cp"]

def shell(cmd):
    print(cmd)
    os.system(cmd)
