from unittest import mock

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app


runner = CliRunner()


def test_off(mock_request: mock.MagicMock) -> None:
    result = runner.invoke(app, ["power", "off"])

    mock_request.assert_called_once_with("ssap://system/turnOff")
    assert result.exit_code == 0
    assert result.stdout == ""


@mock.patch("alga.cli_power.send_magic_packet")
def test_on(mock_send_magic_packet: mock.MagicMock, faker: Faker) -> None:
    mac_address = faker.pystr()

    result = runner.invoke(app, ["power", "on", mac_address])

    mock_send_magic_packet.assert_called_once_with(mac_address)
    assert result.exit_code == 0
    assert result.stdout == ""
