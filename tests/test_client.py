import json
import ssl
from unittest.mock import ANY, MagicMock, call, patch

import pytest
from faker import Faker
from typer import Exit

from alga import client
from alga.payloads import get_hello_data


def test_connect(faker: Faker) -> None:
    hostname = faker.pystr()
    timeout = faker.pyint()

    with patch("alga.client.WebSocket") as mock_websocket:
        mock_websocket

        with client.connect(hostname, timeout):
            pass

    mock_websocket.assert_has_calls(
        [
            call(sslopt={"cert_reqs": ssl.CERT_NONE}),
            call().connect(
                f"wss://{hostname}:3001/", suppress_origin=True, timeout=timeout
            ),
            call().close(),
        ]
    )


def test_do_handshake(faker: Faker) -> None:
    key = faker.pystr()
    mock_connection = MagicMock()

    mock_connection.recv.return_value = json.dumps(
        {"payload": {"client-key": faker.pystr()}}
    )

    client.do_handshake(mock_connection, key)

    mock_connection.send.assert_called_once_with(json.dumps(get_hello_data(key)))


def test_do_handshake_error(faker: Faker) -> None:
    key = faker.pystr()
    mock_connection = MagicMock()

    mock_connection.recv.return_value = json.dumps({"payload": {}})

    with pytest.raises(
        Exception, match="Something went wrong with performing a handshake"
    ):
        client.do_handshake(mock_connection, key)


def test_request_no_config(faker: Faker, mock_config: MagicMock) -> None:
    mock_config.return_value = {}

    with pytest.raises(Exit) as exc_info:
        client.request(faker.pystr())

    assert exc_info.value.exit_code == 1


def test_request_tv_id_not_in_config(faker: Faker, mock_config: MagicMock) -> None:
    mock_config.return_value = {"default_tv": faker.pystr(), "tvs": {}}

    with pytest.raises(Exit) as exc_info:
        client.request(faker.pystr())

    assert exc_info.value.exit_code == 1


def test_request_no_data(faker: Faker, mock_config: MagicMock) -> None:
    name, hostname, key = faker.pystr(), faker.pystr(), faker.pystr()
    mock_config.return_value = {
        "default_tv": name,
        "tvs": {name: {"hostname": hostname, "key": key}},
    }

    uri = faker.pystr()
    payload = {"returnValue": True} | faker.pydict()

    with patch("alga.client.connect") as mock_connect:
        mock_connect().__enter__().recv.side_effect = [
            json.dumps({"payload": {"client-key": faker.pystr()}}),
            json.dumps({"payload": payload}),
        ]

        response = client.request(uri)

        assert response == payload

        mock_connect().__enter__().send.assert_has_calls(
            [
                call(ANY),  # Handshake
                call(json.dumps({"type": "request", "uri": uri})),
            ]
        )


def test_request_with_data(faker: Faker, mock_config: MagicMock) -> None:
    name, hostname, key = faker.pystr(), faker.pystr(), faker.pystr()
    mock_config.return_value = {
        "default_tv": name,
        "tvs": {name: {"hostname": hostname, "key": key}},
    }

    uri, data = faker.pystr(), faker.pydict(allowed_types=[str, float, int])
    payload = {"returnValue": True} | faker.pydict()

    with patch("alga.client.connect") as mock_connect:
        mock_connect().__enter__().recv.side_effect = [
            json.dumps({"payload": {"client-key": faker.pystr()}}),
            json.dumps({"payload": payload}),
        ]

        response = client.request(uri, data)

        assert response == payload

        mock_connect().__enter__().send.assert_has_calls(
            [
                call(ANY),  # Handshake
                call(json.dumps({"type": "request", "uri": uri, "payload": data})),
            ]
        )
