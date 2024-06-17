from typer import Typer
from wakeonlan import send_magic_packet

from alga import client, config


app = Typer(no_args_is_help=True, help="Turn TV screen on and off")


@app.command()
def off() -> None:
    """Turn TV screen off"""

    client.request("ssap://com.webos.service.tvpower/power/turnOffScreen")

@app.command()
def on() -> None:
    """Turn TV screen on"""

    client.request("ssap://com.webos.service.tvpower/power/turnOnScreen")

