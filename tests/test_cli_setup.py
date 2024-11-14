from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, gaierror
from unittest import mock

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app
from alga.cli_setup import _ip_from_hostname


runner = CliRunner()


@mock.patch("alga.cli_setup.getaddrinfo")
def test_ip_from_hostname(mock_getaddrinfo: mock.MagicMock, faker: Faker) -> None:
    hostname = faker.hostname()
    ip_address = faker.ipv4()

    mock_getaddrinfo.return_value = [
        (AF_INET, SOCK_DGRAM, 17, "", (ip_address, 0)),
        (AF_INET, SOCK_STREAM, 6, "", (ip_address, 0)),
    ]

    result = _ip_from_hostname(hostname)

    mock_getaddrinfo.assert_called_once_with(host=hostname, port=None)
    assert result == ip_address


@mock.patch("alga.cli_setup.getaddrinfo")
def test_ip_from_hostname_not_found(
    mock_getaddrinfo: mock.MagicMock, faker: Faker
) -> None:
    hostname = faker.hostname()
    mock_getaddrinfo.side_effect = gaierror(
        "[Errno 8] nodename nor servname provided, or not known"
    )

    result = _ip_from_hostname(hostname)

    mock_getaddrinfo.assert_called_once_with(host=hostname, port=None)
    assert result is None


@mock.patch("alga.cli_setup._ip_from_hostname")
def test_setup_ip_not_found(
    mock_ip_from_hostname: mock.MagicMock, faker: Faker
) -> None:
    hostname = faker.hostname()
    mock_ip_from_hostname.return_value = None

    result = runner.invoke(app, ["setup", hostname])

    mock_ip_from_hostname.assert_called_once_with(hostname)
    assert result.exit_code == 1
    assert (
        result.stdout.replace("\n", "")
        == f"Could not find any host by the name '{hostname}'. Is the TV on and connected to the network?"
    )
