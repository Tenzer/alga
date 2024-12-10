import json
import ssl
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Optional, cast

from rich import print
from typer import Exit
from websocket import WebSocket

from alga import config, state
from alga.payloads import get_hello_data


@contextmanager
def connect(hostname: str, timeout: int = 10) -> Iterator[WebSocket]:
    connection = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    connection.connect(f"wss://{hostname}:3001/", suppress_origin=True, timeout=timeout)  # type: ignore[no-untyped-call]

    try:
        yield connection
    finally:
        connection.close()


def do_handshake(connection: WebSocket, key: str) -> None:
    connection.send(json.dumps(get_hello_data(key)))
    response = json.loads(connection.recv())
    if "client-key" not in response["payload"]:
        raise Exception(
            f"Something went wrong with performing a handshake. Response: {response}"
        )


def request(uri: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    cfg = config.get()
    tv_id = state.tv_id or cfg.get("default_tv")

    if not tv_id:
        print("[red]No connection configured, run 'alga tv add' first[/red]")
        raise Exit(code=1)

    if tv_id not in cfg["tvs"]:
        print(f"[red]'{tv_id}' was not found in the configuration[/red]")
        raise Exit(code=1)

    tv = cfg["tvs"][tv_id]

    with connect(tv["hostname"]) as connection:
        do_handshake(connection, tv["key"])

        request: dict[str, Any] = {"type": "request", "uri": uri}

        if data:
            request.update(payload=data)

        connection.send(json.dumps(request))

        raw_response = connection.recv()
        response = json.loads(raw_response)

        assert response.get("payload", {}).get("returnValue") is True
        return cast(dict[str, Any], response["payload"])
