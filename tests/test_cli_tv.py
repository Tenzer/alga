from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, gaierror
from unittest.mock import MagicMock, patch

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app
from alga.cli_tv import _ip_from_hostname


runner = CliRunner()


@patch("alga.cli_tv.getaddrinfo")
def test_ip_from_hostname(mock_getaddrinfo: MagicMock, faker: Faker) -> None:
    hostname = faker.hostname()
    ip_address = faker.ipv4()

    mock_getaddrinfo.return_value = [
        (AF_INET, SOCK_DGRAM, 17, "", (ip_address, 0)),
        (AF_INET, SOCK_STREAM, 6, "", (ip_address, 0)),
    ]

    result = _ip_from_hostname(hostname)

    mock_getaddrinfo.assert_called_once_with(host=hostname, port=None)
    assert result == ip_address


@patch("alga.cli_tv.getaddrinfo")
def test_ip_from_hostname_not_found(mock_getaddrinfo: MagicMock, faker: Faker) -> None:
    hostname = faker.hostname()
    mock_getaddrinfo.side_effect = gaierror(
        "[Errno 8] nodename nor servname provided, or not known"
    )

    result = _ip_from_hostname(hostname)

    mock_getaddrinfo.assert_called_once_with(host=hostname, port=None)
    assert result is None


@patch("alga.cli_tv._ip_from_hostname")
def test_add_ip_not_found(mock_ip_from_hostname: MagicMock, faker: Faker) -> None:
    hostname = faker.hostname()
    mock_ip_from_hostname.return_value = None

    result = runner.invoke(app, ["tv", "add", "name", hostname])

    mock_ip_from_hostname.assert_called_once_with(hostname)
    assert result.exit_code == 1
    assert (
        result.stdout.replace("\n", "")
        == f"Could not find any host by the name '{hostname}'. Is the TV on and connected to the network?"
    )


def test_list(faker: Faker, mock_config: MagicMock) -> None:
    mock_config.return_value = {
        "default_tv": faker.pystr(),
        "tvs": {faker.pystr(): {"hostname": faker.pystr(), "mac": faker.pystr()}},
    }

    result = runner.invoke(app, ["tv", "list"])

    assert result.exit_code == 0


def test_remove(faker: Faker, mock_config: MagicMock) -> None:
    name = faker.pystr()
    mock_config.return_value = {"default_tv": name, "tvs": {name: {}}}

    with patch("alga.cli_tv.config.write") as mock_write:
        result = runner.invoke(app, ["tv", "remove", name])

    assert result.exit_code == 0
    mock_write.assert_called_once_with({"default_tv": "", "tvs": {}})


def test_remove_not_found(faker: Faker, mock_config: MagicMock) -> None:
    mock_config.return_value = {"default_tv": "", "tvs": {}}
    name = faker.pystr()

    result = runner.invoke(app, ["tv", "remove", name])

    assert result.exit_code == 1


def test_rename(faker: Faker, mock_config: MagicMock) -> None:
    old_name, new_name = faker.pystr(), faker.pystr()
    mock_config.return_value = {"default_tv": old_name, "tvs": {old_name: {}}}

    with patch("alga.cli_tv.config.write") as mock_write:
        result = runner.invoke(app, ["tv", "rename", old_name, new_name])

    assert result.exit_code == 0
    mock_write.assert_called_once_with({"default_tv": new_name, "tvs": {new_name: {}}})


def test_rename_not_found(faker: Faker, mock_config: MagicMock) -> None:
    mock_config.return_value = {"default_tv": "", "tvs": {}}
    old_name, new_name = faker.pystr(), faker.pystr()

    result = runner.invoke(app, ["tv", "rename", old_name, new_name])

    assert result.exit_code == 1


def test_set_default(faker: Faker, mock_config: MagicMock) -> None:
    name = faker.pystr()
    mock_config.return_value = {"default_tv": "", "tvs": {name: {}}}

    with patch("alga.cli_tv.config.write") as mock_write:
        result = runner.invoke(app, ["tv", "set-default", name])

    assert result.exit_code == 0
    mock_write.assert_called_once_with({"default_tv": name, "tvs": {name: {}}})


def test_set_default_not_found(faker: Faker, mock_config: MagicMock) -> None:
    name = faker.pystr()
    mock_config.return_value = {"default_tv": "", "tvs": {}}

    result = runner.invoke(app, ["tv", "set-default", name])

    assert result.exit_code == 1
