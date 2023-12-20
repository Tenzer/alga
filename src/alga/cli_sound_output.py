import typer

from alga import client


app = typer.Typer(no_args_is_help=True)


@app.command()
def get() -> None:
    response = client.request("ssap://audio/getSoundOutput")
    typer.echo(f"The current sound output is {response['soundOutput']}")


@app.command()
def set(value: str) -> None:
    client.request("ssap://audio/changeSoundOutput", {"output": value})
