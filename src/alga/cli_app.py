from typing import Annotated, Optional

from rich import print
from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from alga import client


app = Typer(no_args_is_help=True)


@app.command()
def current() -> None:
    response = client.request(
        "ssap://com.webos.applicationManager/getForegroundAppInfo"
    )
    print(f"The current app is [bold]{response['appId']}[/bold]")


@app.command()
def close(app_id: Annotated[str, Argument()]) -> None:
    client.request("ssap://system.launcher/close")


@app.command()
def launch(
    app_id: Annotated[str, Argument()],
    content: Annotated[Optional[str], Argument()] = None,
) -> None:
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


@app.command()
def info(app_id: str) -> None:
    response = client.request(
        "ssap://com.webos.applicationManager/getAppInfo", {"id": app_id}
    )

    print(response["appInfo"])
