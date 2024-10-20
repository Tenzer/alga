from unittest.mock import MagicMock

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app


runner = CliRunner()


def test_send(faker: Faker, mock_input: MagicMock) -> None:
    button = faker.pystr()

    result = runner.invoke(app, ["remote", "send", button])

    mock_input.assert_called_once_with(f"type:button\nname:{button.upper()}\n\n")
    assert result.exit_code == 0
    assert result.stdout == ""
