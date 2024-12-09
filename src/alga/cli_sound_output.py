from typing import Annotated

from pzp import pzp
from rich import print
from typer import Argument, Typer

from alga import client
from alga.types import SoundOutputDevice


app = Typer(no_args_is_help=True, help="Audio output device")


@app.command()
def get() -> None:
    """Show the current output device"""

    response = client.request("ssap://audio/getSoundOutput")
    print(f"The current sound output is [bold]{response['soundOutput']}[/bold]")


@app.command()
def pick() -> None:
    """Show picker for selecting a sound output device."""

    sound_output_device = pzp(
        candidates=[
            SoundOutputDevice("tv_speaker", "TV Speaker"),
            SoundOutputDevice("external_optical", "Optical Out Device"),
            SoundOutputDevice("tv_external_speaker", "Optical Out Device + TV Speaker"),
            SoundOutputDevice("external_arc", "HDMI (ARC) Device"),
        ],
        fullscreen=False,
        layout="reverse",
    )
    if sound_output_device:
        client.request(
            "ssap://audio/changeSoundOutput", {"output": sound_output_device.id_}
        )


@app.command()
def set(value: Annotated[str, Argument()]) -> None:
    """Change the output device"""

    client.request("ssap://audio/changeSoundOutput", {"output": value})
