from typing import Annotated

from rich import print
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from alga import client


app = Typer(no_args_is_help=True)


@app.command()
def current() -> None:
    response = client.request("ssap://tv/getCurrentChannel")
    print(
        f"The current channel is [bold]{response['channelName']}[/bold] ([italic]{response['channelNumber']}[/italic])"
    )


@app.command()
def up() -> None:
    client.request("ssap://tv/channelUp")


@app.command()
def down() -> None:
    client.request("ssap://tv/channelDown")


@app.command()
def set(value: Annotated[int, Argument()]) -> None:
    client.request("ssap://tv/openChannel", {"channelNumber": value})


@app.command()
def list() -> None:
    response = client.request("ssap://tv/getChannelList")

    table = Table()
    table.add_column("Type")
    table.add_column("Number")
    table.add_column("Name")

    all_channels = []
    type_to_emoji = {1: "📺", 2: "📻"}
    for channel in response["channelList"]:
        # The first item is for sorting
        all_channels.append(
            [
                int(channel["channelNumber"]),
                type_to_emoji.get(channel["channelTypeId"], "❓"),
                channel["channelNumber"],
                channel["channelName"],
            ]
        )

    for row in sorted(all_channels):
        table.add_row(*row[1:])

    console = Console()
    console.print(table)
