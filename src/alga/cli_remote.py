import ssl
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Annotated

from typer import Argument, Typer
from websocket import WebSocket

from alga import client


app = Typer(no_args_is_help=True, help="Remote control button presses")


@contextmanager
def _input_connection() -> Iterator[WebSocket]:  # pragma: no cover
    response = client.request(
        "ssap://com.webos.service.networkinput/getPointerInputSocket"
    )

    connection = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    connection.connect(response["socketPath"], suppress_origin=True, timeout=3)  # type: ignore[no-untyped-call]

    try:
        yield connection
    finally:
        connection.close()


@app.command()
def send(button: Annotated[str, Argument()]) -> None:
    """Send a button press to the TV"""
    with _input_connection() as connection:
        connection.send(f"type:button\nname:{button.upper()}\n\n")
