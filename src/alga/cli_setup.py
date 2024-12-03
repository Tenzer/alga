import json
from ipaddress import ip_address
from socket import gaierror, getaddrinfo
from typing import Annotated, Optional

from getmac import get_mac_address
from rich import print
from rich.console import Console
from typer import Argument, Exit, Typer

from alga import client, config
from alga.payloads import get_hello_data


app = Typer()


def _ip_from_hostname(hostname: str) -> Optional[str]:
    try:
        results = getaddrinfo(host=hostname, port=None)
        # TODO: Do we want to handle receiving multiple IP addresses?
        return results[0][4][0]
    except gaierror:
        return None


@app.command()
def setup(
    hostname: Annotated[str, Argument()] = "lgwebostv",
) -> None:  # pragma: no cover
    """Pair a new TV"""

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
        hostname=hostname, perform_handshake=False, timeout=60
    ) as connection:
        connection.send(json.dumps(get_hello_data()))
        response = json.loads(connection.recv())
        assert response == {
            "id": "register_0",
            "payload": {"pairingType": "PROMPT", "returnValue": True},
            "type": "response",
        }, "Unexpected response received"

        console = Console()
        with console.status("Please approve the connection request on the TV now..."):
            response = json.loads(connection.recv())

    if "client-key" not in response["payload"]:
        print("[red]Setup failed![/red]")
        raise Exit(code=1)

    mac_address = get_mac_address(ip=ip)

    cfg = config.get()
    cfg.update(
        hostname=hostname, key=response["payload"]["client-key"], mac=mac_address
    )
    config.write(cfg)

    print("TV configured, Alga is ready to use")
