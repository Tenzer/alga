from typer import Typer
from wakeonlan import send_magic_packet

from alga import client, config


app = Typer(no_args_is_help=True, help="Turn TV (or screen) on and off")


@app.command()
def off() -> None:
    """Turn TV off"""

    client.request("ssap://system/turnOff")


@app.command()
def on() -> None:
    """Turn TV on via Wake-on-LAN"""

    cfg = config.get()
    send_magic_packet(cfg["mac"])


@app.command()
def screen_off() -> None:
    """Turn TV screen off"""

    client.request("ssap://com.webos.service.tvpower/power/turnOffScreen")


@app.command()
def screen_on() -> None:
    """Turn TV screen on"""

    client.request("ssap://com.webos.service.tvpower/power/turnOnScreen")
