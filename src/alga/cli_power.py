from typer import Typer
from wakeonlan import send_magic_packet

from alga import client, config


app = Typer(no_args_is_help=True)


@app.command()
def off() -> None:
    client.request("ssap://system/turnOff")


@app.command()
def on() -> None:
    cfg = config.get()
    send_magic_packet(cfg["mac"])
