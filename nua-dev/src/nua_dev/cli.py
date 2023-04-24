# SPDX-FileCopyrightText: 2023 Abilian SAS <https://abilian.com/>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.metadata

from cleez import CLI


def main():
    version = importlib.metadata.version("nua-dev")
    cli = CLI(name="nua-dev", version=version)

    cli.scan("nua_dev.commands")
    cli.run()
