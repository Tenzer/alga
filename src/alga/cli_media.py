from typer import Typer

from alga import client


app = Typer(no_args_is_help=True)


@app.command()
def play() -> None:
    client.request("ssap://media.controls/play")


@app.command()
def pause() -> None:
    client.request("ssap://media.controls/pause")


@app.command()
def stop() -> None:
    client.request("ssap://media.controls/stop")


@app.command()
def fast_forward() -> None:
    client.request("ssap://media.controls/fastForward")


@app.command()
def rewind() -> None:
    client.request("ssap://media.controls/rewind")
