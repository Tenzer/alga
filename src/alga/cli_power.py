import typer

from alga import client


app = typer.Typer(no_args_is_help=True)


@app.command()
def off() -> None:
    client.request("ssap://system/turnOff")
