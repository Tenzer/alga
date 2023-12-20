import typer

from alga import client


app = typer.Typer(no_args_is_help=True)


@app.command()
def up() -> None:
    client.request("ssap://audio/volumeUp")


@app.command()
def down() -> None:
    client.request("ssap://audio/volumeDown")


@app.command()
def set(value: int) -> None:
    client.request("ssap://audio/setVolume", {"volume": value})


@app.command()
def get() -> None:
    response = client.request("ssap://audio/getVolume")
    typer.echo(
        f"Volume is currently set to {response['volume']} and is currently {'' if response['muted'] else 'not '}muted"
    )


@app.command()
def mute() -> None:
    client.request("ssap://audio/setMute", {"mute": True})


@app.command()
def unmute() -> None:
    client.request("ssap://audio/setMute", {"mute": False})
