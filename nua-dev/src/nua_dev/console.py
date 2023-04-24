import typer
from cleez.colors import red


def panic(msg):
    print(red(msg))
    raise typer.Exit(1)
