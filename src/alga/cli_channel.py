from typing import Annotated

from pzp import pzp
from rich import print
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from alga import client
from alga.types import Channel


app = Typer(no_args_is_help=True, help="TV channels")


@app.command()
def current() -> None:
    """Get the current channel"""

    response = client.request("ssap://tv/getCurrentChannel")
    print(
        f"The current channel is [bold]{response['channelName']}[/bold] ([italic]{response['channelNumber']}[/italic])"
    )


@app.command()
def down() -> None:
    """Change channel down"""

    client.request("ssap://tv/channelDown")


@app.command()
def list() -> None:
    """List available channels"""

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


@app.command()
def pick() -> None:
    """Show picker for selecting a channel."""

    response = client.request("ssap://tv/getChannelList")
    channels = []

    for channel in response["channelList"]:
        channels.append(Channel(channel))

    channel = pzp(candidates=channels, fullscreen=False, layout="reverse")
    if channel:
        client.request("ssap://tv/openChannel", {"channelId": channel.id_})


@app.command()
def set(value: Annotated[str, Argument()]) -> None:
    """Change to specific channel"""

    if value.isnumeric():
        # If a channel number is provided, we look up the channel ID as some models require it.
        response = client.request("ssap://tv/getChannelList")

        for channel in response["channelList"]:
            if channel["channelNumber"] == value:
                value = channel["channelId"]
                break

    client.request("ssap://tv/openChannel", {"channelId": value})


@app.command()
def up() -> None:
    """Change channel up"""

    client.request("ssap://tv/channelUp")
