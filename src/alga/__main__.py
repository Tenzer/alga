from typing import Annotated, Optional

from typer import Option, Typer

from alga import (
    cli_adhoc,
    cli_app,
    cli_channel,
    cli_input,
    cli_media,
    cli_power,
    cli_remote,
    cli_sound_output,
    cli_tv,
    cli_version,
    cli_volume,
    state,
)


def global_options(
    tv: Annotated[
        Optional[str], Option(help="Specify which TV the command should be sent to")
    ] = None,
) -> None:
    state.tv_id = tv


app = Typer(no_args_is_help=True, callback=global_options)
app.add_typer(cli_adhoc.app)
app.add_typer(cli_app.app, name="app")
app.add_typer(cli_channel.app, name="channel")
app.add_typer(cli_input.app, name="input")
app.add_typer(cli_media.app, name="media")
app.add_typer(cli_power.app, name="power")
app.add_typer(cli_remote.app, name="remote")
app.add_typer(cli_sound_output.app, name="sound-output")
app.add_typer(cli_tv.app, name="tv")
app.add_typer(cli_version.app)
app.add_typer(cli_volume.app, name="volume")


if __name__ == "__main__":
    app()
