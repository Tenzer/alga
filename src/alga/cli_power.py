from typer import Typer
from wakeonlan import send_magic_packet

from alga import client


app = Typer(no_args_is_help=True)


@app.command()
def off() -> None:
    client.request("ssap://system/turnOff")


@app.command()
def on(mac: str) -> None:
    send_magic_packet(mac)
