from typing import Annotated

from rich import print
from typer import Argument, Typer

from alga import client


app = Typer(no_args_is_help=True)


@app.command()
def up() -> None:
    client.request("ssap://audio/volumeUp")


@app.command()
def down() -> None:
    client.request("ssap://audio/volumeDown")


@app.command()
def set(value: Annotated[int, Argument()]) -> None:
    client.request("ssap://audio/setVolume", {"volume": value})


@app.command()
def get() -> None:
    response = client.request("ssap://audio/getVolume")
    print(
        f"Volume is currently set to [bold]{response['volume']}[/bold] and is currently {'[red]' if response['muted'] else '[green]not '}muted"
    )


@app.command()
def mute() -> None:
    client.request("ssap://audio/setMute", {"mute": True})


@app.command()
def unmute() -> None:
    client.request("ssap://audio/setMute", {"mute": False})
