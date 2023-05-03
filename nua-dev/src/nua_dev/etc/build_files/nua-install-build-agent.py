#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

args = [sys.executable, "-m", "pip", "install"]

if wheels := Path("/nua/build/dist/").glob("*.whl"):
    subprocess.check_call(args + [str(w) for w in wheels])
else:
    subprocess.check_call([*args, "nua-build-agent"])
