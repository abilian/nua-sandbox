import importlib.metadata
import sys
import traceback

import typer


def get_version() -> str:
    return importlib.metadata.version("nua_agent")


def print_version() -> None:
    typer.echo(f"Nua Agent version: {get_version()}")


class Fail(Exception):
    def __init__(self, msg: str, exception: Exception|None = None):
        typer.secho(msg, fg=typer.colors.RED)
        if exception:
            traceback.print_exception(exception)
            raise typer.Exit(1)

        exc_info = sys.exc_info()
        if exc_info:
            traceback.print_exc()

        raise typer.Exit(1)
