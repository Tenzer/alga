from unittest.mock import MagicMock, call, patch

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app
from alga.types import InputDevice


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


def test_pick(faker: Faker, mock_request: MagicMock) -> None:
    return_value = {
        "devices": [
            {"id": faker.pystr(), "label": faker.pystr()},
            {"id": faker.pystr(), "label": faker.pystr()},
            {"id": faker.pystr(), "label": faker.pystr()},
        ]
    }
    mock_request.return_value = return_value
    first_input = return_value["devices"][0]

    with patch("alga.cli_input.pzp") as mock_pzp:
        mock_pzp.return_value = InputDevice(first_input)

        result = runner.invoke(app, ["input", "pick"])

    mock_request.assert_has_calls(
        [
            call("ssap://tv/getExternalInputList"),
            call("ssap://tv/switchInput", {"inputId": first_input["id"]}),
        ]
    )
    assert result.exit_code == 0
