from unittest.mock import MagicMock, call, patch

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app
from alga.types import Channel


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


def test_set_channel_id(faker: Faker, mock_request: MagicMock) -> None:
    channel_id = faker.pystr()

    result = runner.invoke(app, ["channel", "set", channel_id])

    mock_request.assert_called_once_with(
        "ssap://tv/openChannel", {"channelId": channel_id}
    )
    assert result.exit_code == 0
    assert result.stdout == ""


def test_set_channel_number(faker: Faker, mock_request: MagicMock) -> None:
    channel_number = str(faker.pyint())
    channel_id = faker.pystr()

    mock_request.return_value = {
        "channelList": [{"channelId": channel_id, "channelNumber": channel_number}]
    }

    result = runner.invoke(app, ["channel", "set", channel_number])

    mock_request.assert_called_with("ssap://tv/openChannel", {"channelId": channel_id})
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


def test_pick(faker: Faker, mock_request: MagicMock) -> None:
    return_value = {
        "channelList": [
            {
                "channelId": faker.pystr(),
                "channelName": faker.pystr(),
                "channelNumber": f"{faker.pyint()}",
            },
            {
                "channelId": faker.pystr(),
                "channelName": faker.pystr(),
                "channelNumber": f"{faker.pyint()}",
            },
            {
                "channelId": faker.pystr(),
                "channelName": faker.pystr(),
                "channelNumber": f"{faker.pyint()}",
            },
        ]
    }
    mock_request.return_value = return_value
    first_channel = return_value["channelList"][0]

    with patch("alga.cli_channel.pzp") as mock_pzp:
        mock_pzp.return_value = Channel(first_channel)

        result = runner.invoke(app, ["channel", "pick"])

    mock_request.assert_has_calls(
        [
            call("ssap://tv/getChannelList"),
            call("ssap://tv/openChannel", {"channelId": first_channel["channelId"]}),
        ]
    )
    assert result.exit_code == 0
