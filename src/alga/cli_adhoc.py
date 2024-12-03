import json
from typing import Annotated, Optional

from rich import print
from typer import Argument, Typer

from alga import client


app = Typer()


@app.command()
def adhoc(path: str, data: Annotated[Optional[str], Argument()] = None) -> None:
    """Send raw request to the TV"""

    if data:
        print(client.request(path, json.loads(data)))
    else:
        print(client.request(path))
