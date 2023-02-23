# FIXME: duplicated from nua-agent
import sys
import traceback

import typer


class Fail(Exception):
    def __init__(self, msg: str, exception: Exception | None = None):
        typer.secho(msg, fg=typer.colors.RED)
        if exception:
            traceback.print_exception(exception)
            raise typer.Exit(1)

        exc_info = sys.exc_info()
        if exc_info:
            traceback.print_exc()

        raise typer.Exit(1)
