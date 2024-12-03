from rich import print
from typer import Typer

from alga import __version__


app = Typer()


@app.command()
def version() -> None:
    """Print Alga version"""

    print(f"alga version [bold]{__version__}[/bold]")
