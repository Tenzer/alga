import json
from typing import Annotated, Optional

from rich import print
from typer import Argument

from alga import client


def adhoc(path: str, data: Annotated[Optional[str], Argument()] = None) -> None:
    if data:
        print(client.request(path, json.loads(data)))
    else:
        print(client.request(path))
