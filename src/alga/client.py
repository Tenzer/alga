import json
import ssl
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Optional, cast

from rich import print
from typer import Exit
from websocket import WebSocket

from alga import config
from alga.payloads import get_hello_data


@contextmanager
def new(
    hostname: Optional[str] = None, perform_handshake: bool = True, timeout: int = 3
) -> Iterator[WebSocket]:  # pragma: no cover
    cfg = config.get()

    if hostname is None:
        if "hostname" not in cfg:
            print("[red]No connection configured, run 'alga setup' first[/red]")
            raise Exit(code=1)

        hostname = cfg["hostname"]

    connection = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    connection.connect(f"wss://{hostname}:3001/", suppress_origin=True, timeout=timeout)  # type: ignore[no-untyped-call]

    if perform_handshake:
        if "key" not in cfg:
            print("[red]No connection configured, run 'alga setup' first[/red]")
            raise Exit(code=1)

        connection.send(json.dumps(get_hello_data(cfg["key"])))
        response = json.loads(connection.recv())
        if "client-key" not in response["payload"]:
            raise Exception(
                f"Something went wrong with performing a handshake. Response: {response}"
            )

    try:
        yield connection
    finally:
        connection.close()


def request(
    uri: str, data: Optional[dict[str, Any]] = None
) -> dict[str, Any]:  # pragma: no cover
    with new() as connection:
        request: dict[str, Any] = {"type": "request", "uri": uri}

        if data:
            request.update(payload=data)

        connection.send(json.dumps(request))

        raw_response = connection.recv()
        response = json.loads(raw_response)

        assert response.get("payload", {}).get("returnValue") is True
        return cast(dict[str, Any], response["payload"])
