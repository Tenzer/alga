import json
import ssl
from collections.abc import Iterator
from contextlib import contextmanager
from os import getenv
from typing import Any, cast

from websocket import WebSocket

from alga.payloads import get_hello_data


HOSTNAME = getenv("ALGA_HOST", "lgwebostv")
KEY = getenv("ALGA_KEY", "")


@contextmanager
def new() -> Iterator[WebSocket]:
    connection = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    connection.connect(f"wss://{HOSTNAME}:3001/", suppress_origin=True, timeout=3)  # type: ignore[no-untyped-call]

    connection.send(json.dumps(get_hello_data(KEY)))
    response = json.loads(connection.recv())
    if "client-key" not in response["payload"]:
        print("Handshake response payload:", response)
        raise Exception("Something went wrong with performing a handshake")

    try:
        yield connection
    finally:
        connection.close()


def request(uri: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    with new() as conn:
        request: dict[str, Any] = {"type": "request", "uri": uri}

        if data:
            request.update(payload=data)

        conn.send(json.dumps(request))

        raw_response = conn.recv()
        response = json.loads(raw_response)

        assert response.get("payload", {}).get("returnValue") is True
        return cast(dict[str, Any], response["payload"])
