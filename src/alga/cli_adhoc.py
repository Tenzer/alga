import json
from typing import Annotated

from rich import print_json
from typer import Argument, Typer

from alga import client


app = Typer()


@app.command()
def adhoc(path: str, data: Annotated[str | None, Argument()] = None) -> None:
    """Send raw request to the TV"""

    data_str = json.loads(data) if data else None
    print_json(data=client.request(path, data_str))
