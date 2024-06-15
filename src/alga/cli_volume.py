from typing import Annotated

from rich import print
from typer import Argument, Typer

from alga import client


app = Typer(no_args_is_help=True, help="Audio volume")


@app.command()
def up() -> None:
    """Turn volume up"""

    client.request("ssap://audio/volumeUp")


@app.command()
def down() -> None:
    """Turn volume down"""

    client.request("ssap://audio/volumeDown")


@app.command()
def set(value: Annotated[int, Argument()]) -> None:
    """Set volume to specific amount"""

    client.request("ssap://audio/setVolume", {"volume": value})


@app.command()
def get() -> None:
    """Get current volume"""

    response = client.request("ssap://audio/getVolume")
    print(
        f"Volume is currently set to [bold]{response['volume']}[/bold] and is currently {'[red]' if response['muted'] else '[green]not '}muted"
    )


@app.command()
def mute() -> None:
    """Mute audio"""

    client.request("ssap://audio/setMute", {"mute": True})


@app.command()
def unmute() -> None:
    """Unmute audio"""

    client.request("ssap://audio/setMute", {"mute": False})
