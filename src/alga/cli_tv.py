import json
from ipaddress import ip_address
from socket import gaierror, getaddrinfo
from typing import Annotated, Optional, cast

from getmac import get_mac_address
from rich import print
from rich.console import Console
from rich.table import Table
from typer import Argument, Exit, Typer

from alga import client, config
from alga.payloads import get_hello_data


def _ip_from_hostname(hostname: str) -> Optional[str]:
    try:
        results = getaddrinfo(host=hostname, port=None)
        # TODO: Do we want to handle receiving multiple IP addresses?
        first_address = results[0]
        sockaddr = first_address[4]
        address = sockaddr[0]
        return cast(str, address)
    except gaierror:
        return None


app = Typer(no_args_is_help=True, help="Set up TVs to manage via Alga")


@app.command()
def add(
    name: Annotated[str, Argument()], hostname: Annotated[str, Argument()] = "lgwebostv"
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

    with client.connect(hostname=hostname, timeout=60) as connection:
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
    cfg["tvs"][name] = {
        "hostname": hostname,
        "key": response["payload"]["client-key"],
        "mac": mac_address,
    }

    if not cfg.get("default_tv"):
        cfg["default_tv"] = name

    config.write(cfg)

    print("TV configured, Alga is ready to use")


@app.command()
def list() -> None:
    """List current TVs"""

    cfg = config.get()

    table = Table()
    table.add_column("Default")
    table.add_column("Name")
    table.add_column("Hostname/IP")
    table.add_column("MAC address")

    for name, tv in cfg["tvs"].items():
        default = "*" if cfg["default_tv"] == name else ""
        table.add_row(default, name, tv["hostname"], tv["mac"])

    console = Console()
    console.print(table)


@app.command()
def remove(name: Annotated[str, Argument()]) -> None:
    """Remove a TV"""

    cfg = config.get()

    try:
        cfg["tvs"].pop(name)

        if cfg["default_tv"] == name:
            cfg["default_tv"] = ""

        config.write(cfg)
    except KeyError:
        print(
            f"[red]A TV with the name '{name}' was not found in the configuration[/red]"
        )
        raise Exit(code=1)


@app.command()
def rename(
    old_name: Annotated[str, Argument()], new_name: Annotated[str, Argument()]
) -> None:
    """Change the identifier for a TV"""

    cfg = config.get()

    try:
        cfg["tvs"][new_name] = cfg["tvs"].pop(old_name)

        if cfg["default_tv"] == old_name:
            cfg["default_tv"] = new_name

        config.write(cfg)
    except KeyError:
        print(
            f"[red]A TV with the name '{old_name}' was not found in the configuration[/red]"
        )
        raise Exit(code=1)


@app.command()
def set_default(name: Annotated[str, Argument()]) -> None:
    """Set the default TV"""

    cfg = config.get()

    if name in cfg["tvs"]:
        cfg["default_tv"] = name
        config.write(cfg)
    else:
        print(
            f"[red]A TV with the name '{name}' was not found in the configuration[/red]"
        )
        raise Exit(code=1)
