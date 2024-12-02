from unittest.mock import MagicMock

import pytest
from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app


runner = CliRunner()


def test_up(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["volume", "up"])

    mock_request.assert_called_once_with("ssap://audio/volumeUp")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_down(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["volume", "down"])

    mock_request.assert_called_once_with("ssap://audio/volumeDown")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_set(faker: Faker, mock_request: MagicMock) -> None:
    volume = faker.pyint()

    result = runner.invoke(app, ["volume", "set", f"{volume}"])

    mock_request.assert_called_once_with("ssap://audio/setVolume", {"volume": volume})
    assert result.exit_code == 0
    assert result.stdout == ""


@pytest.mark.parametrize(
    ["muted", "version"], [[True, "old"], [False, "old"], [True, "new"], [False, "new"]]
)
def test_get(faker: Faker, mock_request: MagicMock, muted: bool, version: str) -> None:
    volume = faker.pyint()
    if version == "old":
        mock_request.return_value = {"volume": volume, "muted": muted}
    else:
        mock_request.return_value = {
            "volumeStatus": {"volume": volume, "muteStatus": muted}
        }

    result = runner.invoke(app, ["volume", "get"])

    mock_request.assert_called_once_with("ssap://audio/getVolume")
    assert result.exit_code == 0

    muted_text = ""
    if not muted:
        muted_text = "not "

    assert (
        result.stdout
        == f"Volume is currently set to {volume} and is currently {muted_text}muted\n"
    )


def test_mute(faker: Faker, mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["volume", "mute"])

    mock_request.assert_called_once_with("ssap://audio/setMute", {"mute": True})
    assert result.exit_code == 0
    assert result.stdout == ""


def test_unmute(faker: Faker, mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["volume", "unmute"])

    mock_request.assert_called_once_with("ssap://audio/setMute", {"mute": False})
    assert result.exit_code == 0
    assert result.stdout == ""
