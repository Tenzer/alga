from rich import print

from alga import __version__


def version() -> None:
    """Print Alga version"""

    print(f"alga version [bold]{__version__}[/bold]")
