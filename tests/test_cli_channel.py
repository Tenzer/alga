from unittest.mock import MagicMock

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app


runner = CliRunner()


def test_current(faker: Faker, mock_request: MagicMock) -> None:
    channel_name = faker.pystr()
    channel_number = faker.pyint()
    mock_request.return_value = {
        "channelName": channel_name,
        "channelNumber": channel_number,
    }

    result = runner.invoke(app, ["channel", "current"])

    mock_request.assert_called_once_with("ssap://tv/getCurrentChannel")
    assert result.exit_code == 0
    assert (
        result.stdout == f"The current channel is {channel_name} ({channel_number})\n"
    )


def test_up(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["channel", "up"])

    mock_request.assert_called_once_with("ssap://tv/channelUp")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_down(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["channel", "down"])

    mock_request.assert_called_once_with("ssap://tv/channelDown")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_set(faker: Faker, mock_request: MagicMock) -> None:
    channel_number = faker.pyint()

    result = runner.invoke(app, ["channel", "set", f"{channel_number}"])

    mock_request.assert_called_once_with(
        "ssap://tv/openChannel", {"channelNumber": channel_number}
    )
    assert result.exit_code == 0
    assert result.stdout == ""


def test_list(faker: Faker, mock_request: MagicMock) -> None:
    return_value = {
        "channelList": [
            {
                "channelNumber": f"{faker.pyint()}",
                "channelTypeId": faker.random_element([1, 2]),
                "channelName": faker.pystr(),
            },
            {
                "channelNumber": f"{faker.pyint()}",
                "channelTypeId": faker.random_element([1, 2]),
                "channelName": faker.pystr(),
            },
            {
                "channelNumber": f"{faker.pyint()}",
                "channelTypeId": faker.random_element([1, 2]),
                "channelName": faker.pystr(),
            },
        ]
    }
    mock_request.return_value = return_value

    result = runner.invoke(app, ["channel", "list"])

    mock_request.assert_called_once_with("ssap://tv/getChannelList")
    assert result.exit_code == 0

    splitted_output = result.stdout.split("\n")
    assert len(splitted_output) == (
        3  # table header
        + 3  # channels
        + 1  # table footer
        + 1  # trailing newline
    )
