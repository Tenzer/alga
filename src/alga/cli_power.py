from typer import Typer

from alga import client


app = Typer(no_args_is_help=True)


@app.command()
def off() -> None:
    client.request("ssap://system/turnOff")
