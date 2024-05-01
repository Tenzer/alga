from unittest.mock import MagicMock

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app


runner = CliRunner()


def test_set(faker: Faker, mock_request: MagicMock) -> None:
    input_name = faker.pystr()

    result = runner.invoke(app, ["input", "set", input_name])

    mock_request.assert_called_once_with(
        "ssap://tv/switchInput", {"inputId": input_name}
    )
    assert result.exit_code == 0
    assert result.stdout == ""


def test_list(faker: Faker, mock_request: MagicMock) -> None:
    return_value = {
        "devices": [
            {"id": faker.pystr(), "label": faker.pystr()},
            {"id": faker.pystr(), "label": faker.pystr()},
            {"id": faker.pystr(), "label": faker.pystr()},
        ]
    }
    mock_request.return_value = return_value

    result = runner.invoke(app, ["input", "list"])

    mock_request.assert_called_once_with("ssap://tv/getExternalInputList")
    assert result.exit_code == 0

    splitted_output = result.stdout.split("\n")
    assert len(splitted_output) == (
        3  # table header
        + 3  # inputs
        + 1  # table footer
        + 1  # trailing newline
    )
