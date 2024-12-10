from unittest.mock import MagicMock, patch

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app


runner = CliRunner()


def test_off(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["power", "off"])

    mock_request.assert_called_once_with("ssap://system/turnOff")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_screen_off(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["power", "screen-off"])

    mock_request.assert_called_once_with(
        "ssap://com.webos.service.tvpower/power/turnOffScreen"
    )
    assert result.exit_code == 0
    assert result.stdout == ""


def test_screen_on(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["power", "screen-on"])

    mock_request.assert_called_once_with(
        "ssap://com.webos.service.tvpower/power/turnOnScreen"
    )
    assert result.exit_code == 0
    assert result.stdout == ""


def test_on(mock_config: MagicMock, faker: Faker) -> None:
    mac_address = faker.pystr()
    mock_config.return_value = {
        "default_tv": "default",
        "tvs": {"default": {"mac": mac_address}},
    }

    with patch("alga.cli_power.send_magic_packet") as mock_send_magic_packet:
        result = runner.invoke(app, ["power", "on"])

    mock_send_magic_packet.assert_called_once_with(mac_address)
    assert result.exit_code == 0
    assert result.stdout == ""
