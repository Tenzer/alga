from typer.testing import CliRunner

from alga import __version__
from alga.__main__ import app


runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout == f"alga version {__version__}\n"
