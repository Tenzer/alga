from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_request() -> Iterator[MagicMock]:
    with patch("alga.client.request") as mocked:
        yield mocked


@pytest.fixture
def mock_input() -> Iterator[MagicMock]:
    with patch("alga.cli_remote._input_connection") as mocked:
        yield mocked.return_value.__enter__.return_value.send


@pytest.fixture
def mock_config() -> Iterator[MagicMock]:
    with patch("alga.config.get") as mocked:
        yield mocked


@pytest.fixture
def mock_config_file() -> Iterator[MagicMock]:
    with patch("alga.config._config_file") as mocked:
        yield mocked
