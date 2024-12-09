from unittest.mock import MagicMock, patch

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app
from alga.types import SoundOutputDevice


runner = CliRunner()


def test_get(faker: Faker, mock_request: MagicMock) -> None:
    sound_output = faker.pystr()
    mock_request.return_value = {"soundOutput": sound_output}

    result = runner.invoke(app, ["sound-output", "get"])

    mock_request.assert_called_once_with("ssap://audio/getSoundOutput")
    assert result.exit_code == 0
    assert result.stdout == f"The current sound output is {sound_output}\n"


def test_set(faker: Faker, mock_request: MagicMock) -> None:
    sound_output = faker.pystr()

    result = runner.invoke(app, ["sound-output", "set", sound_output])

    mock_request.assert_called_once_with(
        "ssap://audio/changeSoundOutput", {"output": sound_output}
    )
    assert result.exit_code == 0
    assert result.stdout == ""


def test_pick(faker: Faker, mock_request: MagicMock) -> None:
    sound_output_device = SoundOutputDevice(faker.pystr(), faker.pystr())

    with patch("alga.cli_sound_output.pzp") as mock_pzp:
        mock_pzp.return_value = sound_output_device

        result = runner.invoke(app, ["sound-output", "pick"])

    mock_request.assert_called_once_with(
        "ssap://audio/changeSoundOutput", {"output": sound_output_device.id_}
    )
    assert result.exit_code == 0
