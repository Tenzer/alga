import json
from ipaddress import ip_address
from socket import gaierror, getaddrinfo
from typing import Annotated, Optional

from rich import print
from typer import Argument, Exit

from alga import client
from alga.payloads import get_hello_data


def _ip_from_hostname(hostname: str) -> Optional[str]:
    try:
        results = getaddrinfo(host=hostname, port=None)
        # TODO: Do we want to handle receiving multiple IP addresses?
        return results[0][4][0]
    except gaierror:
        return None


def setup(hostname: Annotated[str, Argument()] = "lgwebostv") -> None:
    # Check if we have been passed an IP address
    ip: Optional[str]
    try:
        ip = ip_address(hostname).compressed
    except ValueError:
        ip = _ip_from_hostname(hostname)
        if not ip:
            print(
                f"[red]Could not find any host by the name '{hostname}'.[/red] Is the TV on and connected to the network?"
            )
            raise Exit(code=1)

    with client.new(
        perform_handshake=False, timeout=60
    ) as connection:  # pragma: no cover
        connection.send(json.dumps(get_hello_data()))
        response = json.loads(connection.recv())
        assert response == {
            "id": "register_0",
            "payload": {"pairingType": "PROMPT", "returnValue": True},
            "type": "response",
        }, "Unexpected response received"
        print("Please approve the connection request on the TV now...")

        response = json.loads(connection.recv())
        if "client-key" not in response["payload"]:
            print("[red]Setup failed![/red]")
            raise Exit(code=1)

        print(
            f"Got key: {response['payload']['client-key']}. Please put this in the `ALGA_KEY` environment variable"
        )
