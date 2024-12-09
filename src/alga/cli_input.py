from typing import Annotated

from pzp import pzp
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from alga import client
from alga.types import InputDevice


app = Typer(no_args_is_help=True, help="HDMI and similar inputs")


@app.command()
def list() -> None:
    """List available inputs"""

    response = client.request("ssap://tv/getExternalInputList")

    table = Table()
    table.add_column("Name")
    table.add_column("ID")

    all_inputs = []
    for i in response["devices"]:
        all_inputs.append([i["label"], i["id"]])

    for row in all_inputs:
        table.add_row(*row)

    console = Console()
    console.print(table)


@app.command()
def pick() -> None:
    """Show picker for selecting an input."""

    response = client.request("ssap://tv/getExternalInputList")
    input_devices = []

    for input_device in response["devices"]:
        input_devices.append(InputDevice(input_device))

    input_device = pzp(candidates=input_devices, fullscreen=False, layout="reverse")
    if input_device:
        client.request("ssap://tv/switchInput", {"inputId": input_device.id_})


@app.command()
def set(value: Annotated[str, Argument()]) -> None:
    """Switch to given input"""

    client.request("ssap://tv/switchInput", {"inputId": value})
