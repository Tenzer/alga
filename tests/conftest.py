from collections.abc import Iterator
from unittest import mock

import pytest


@pytest.fixture
def mock_request() -> Iterator[mock.MagicMock]:
    with mock.patch("alga.client.request") as mocked:
        yield mocked


@pytest.fixture
def mock_input() -> Iterator[mock.MagicMock]:
    with mock.patch("alga.cli_remote._input_connection") as mocked:
        yield mocked.return_value.__enter__.return_value.send
