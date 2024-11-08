from typer import Typer

from alga import client


app = Typer(no_args_is_help=True, help="Control the playing media")


@app.command()
def fast_forward() -> None:
    """Fast forward media"""

    client.request("ssap://media.controls/fastForward")


@app.command()
def pause() -> None:
    """Pause media"""

    client.request("ssap://media.controls/pause")


@app.command()
def play() -> None:
    """Play media"""

    client.request("ssap://media.controls/play")


@app.command()
def rewind() -> None:
    """Rewind media"""

    client.request("ssap://media.controls/rewind")


@app.command()
def stop() -> None:
    """Stop media"""

    client.request("ssap://media.controls/stop")
