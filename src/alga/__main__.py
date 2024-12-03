from typer import Typer

from alga import (
    cli_adhoc,
    cli_app,
    cli_channel,
    cli_input,
    cli_media,
    cli_power,
    cli_remote,
    cli_setup,
    cli_sound_output,
    cli_version,
    cli_volume,
)


app = Typer(no_args_is_help=True)
app.add_typer(cli_adhoc.app)
app.add_typer(cli_app.app, name="app")
app.add_typer(cli_channel.app, name="channel")
app.add_typer(cli_input.app, name="input")
app.add_typer(cli_media.app, name="media")
app.add_typer(cli_power.app, name="power")
app.add_typer(cli_remote.app, name="remote")
app.add_typer(cli_setup.app)
app.add_typer(cli_sound_output.app, name="sound-output")
app.add_typer(cli_version.app)
app.add_typer(cli_volume.app, name="volume")


if __name__ == "__main__":
    app()
