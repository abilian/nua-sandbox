import typer
from typer.colors import RED


def panic(msg):
    typer.secho(msg, fg=RED)
    raise typer.Exit(1)
