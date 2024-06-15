from typing import Annotated

from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from alga import client


app = Typer(no_args_is_help=True, help="HDMI and similar inputs")


@app.command()
def set(value: Annotated[str, Argument()]) -> None:
    """Switch to given input"""

    client.request("ssap://tv/switchInput", {"inputId": value})


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
