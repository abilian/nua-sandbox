# SPDX-FileCopyrightText: 2023 Abilian SAS <https://abilian.com/>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.metadata

import snoop
from cleez import CLI
from cleez.actions import VERSION

snoop.install()


def get_cli() -> CLI:
    version = get_version()
    cli = CLI(name="nua-dev", version=version)
    add_default_arguments(cli)
    cli.scan("nua_dev.commands")
    return cli


def get_version():
    return importlib.metadata.version("nua-dev")


def add_default_arguments(cli: CLI):
    cli.add_option(
        "-V",
        "--version",
        action=VERSION,
        version=cli.version,
        help="Show version and exit",
    )
    cli.add_option(
        "-d", "--debug", default=False, action="store_true", help="Enable debug mode"
    )
    cli.add_option(
        "-v", "--verbose", default=False, action="store_true", help="Increase verbosity"
    )


def main():
    cli = get_cli()
    cli.run()
