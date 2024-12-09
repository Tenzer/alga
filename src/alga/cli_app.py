import json
from typing import Annotated, Optional

from pzp import pzp
from rich import print
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from alga import client
from alga.types import App


app = Typer(no_args_is_help=True, help="Apps installed on the TV")


@app.command()
def close(app_id: Annotated[str, Argument()]) -> None:
    """Close the provided app"""

    client.request("ssap://system.launcher/close", {"id": app_id})


@app.command()
def current() -> None:
    """Get the current app"""

    response = client.request(
        "ssap://com.webos.applicationManager/getForegroundAppInfo"
    )
    print(f"The current app is [bold]{response['appId']}[/bold]")


@app.command()
def info(app_id: str) -> None:
    """Show info about specific app"""

    response = client.request(
        "ssap://com.webos.applicationManager/getAppInfo", {"id": app_id}
    )

    print(response["appInfo"])


@app.command()
def launch(
    app_id: Annotated[str, Argument()],
    data: Annotated[Optional[str], Argument()] = None,
) -> None:
    """Launch an app"""

    payload = {"id": app_id}
    if data:
        payload.update(json.loads(data))
    client.request("ssap://system.launcher/launch", payload)


@app.command()
def list() -> None:
    """List installed apps"""

    response = client.request("ssap://com.webos.applicationManager/listApps")

    table = Table()
    table.add_column("Name")
    table.add_column("ID")

    all_apps = []
    for app in response["apps"]:
        all_apps.append([app["title"], app["id"]])

    for row in sorted(all_apps):
        table.add_row(*row)

    console = Console()
    console.print(table)


@app.command()
def pick() -> None:
    """Show picker for selecting an app."""

    response = client.request("ssap://com.webos.applicationManager/listApps")
    apps = []

    for app in response["apps"]:
        apps.append(App(app))

    app = pzp(candidates=apps, fullscreen=False, layout="reverse")
    if app:
        client.request("ssap://system.launcher/launch", {"id": app.id_})
