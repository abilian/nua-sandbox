# SPDX-FileCopyrightText: 2023 Abilian SAS <https://abilian.com/>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.metadata

import snoop
from cleez import CLI

snoop.install()


def get_cli() -> CLI:
    version = importlib.metadata.version("nua-dev")
    cli = CLI(name="nua-dev", version=version)
    cli.scan("nua_dev.commands")
    return cli


def main():
    cli = get_cli()
    cli.run()
