from typing import Annotated

from rich import print
from typer import Argument, Typer

from alga import client


app = Typer(no_args_is_help=True)


@app.command()
def get() -> None:
    response = client.request("ssap://audio/getSoundOutput")
    print(f"The current sound output is [bold]{response['soundOutput']}[/bold]")


@app.command()
def set(value: Annotated[str, Argument()]) -> None:
    client.request("ssap://audio/changeSoundOutput", {"output": value})
