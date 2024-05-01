from collections.abc import Iterator
from unittest import mock

import pytest


@pytest.fixture
def mock_request() -> Iterator[mock.MagicMock]:
    with mock.patch("alga.client.request") as mocked:
        yield mocked
