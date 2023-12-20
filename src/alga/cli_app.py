from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from alga import client


app = typer.Typer(no_args_is_help=True)


@app.command()
def current() -> None:
    response = client.request(
        "ssap://com.webos.applicationManager/getForegroundAppInfo"
    )
    typer.echo(f"The current app is {response['appId']}")


@app.command()
def close(app_id: str) -> None:
    client.request("ssap://system.launcher/close")


@app.command()
def launch(app_id: str, content: Optional[str] = None) -> None:
    client.request("ssap://system.launcher/launch", {"id": app_id})


@app.command()
def list() -> None:
    response = client.request("ssap://com.webos.applicationManager/listApps")

    table = Table()
    table.add_column("Name")
    table.add_column("ID")

    all_apps = []
    for a in response["apps"]:
        all_apps.append([a["title"], a["id"]])

    for row in sorted(all_apps):
        table.add_row(*row)

    console = Console()
    console.print(table)
