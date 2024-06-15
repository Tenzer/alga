from typing import Annotated

from rich import print
from typer import Argument, Typer

from alga import client


app = Typer(no_args_is_help=True, help="Audio output device")


@app.command()
def get() -> None:
    """Show the current output device"""

    response = client.request("ssap://audio/getSoundOutput")
    print(f"The current sound output is [bold]{response['soundOutput']}[/bold]")


@app.command()
def set(value: Annotated[str, Argument()]) -> None:
    """Change the output device"""

    client.request("ssap://audio/changeSoundOutput", {"output": value})
