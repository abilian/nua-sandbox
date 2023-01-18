import importlib.metadata

import typer


def get_version() -> str:
    return importlib.metadata.version("nua_agent")


def print_version() -> None:
    typer.echo(f"Nua Agent version: {get_version()}")
