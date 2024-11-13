import json
from unittest.mock import MagicMock

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app


runner = CliRunner()


def test_without_data(faker: Faker, mock_request: MagicMock) -> None:
    path = faker.pystr()
    return_value = faker.pystr()
    mock_request.return_value = return_value

    result = runner.invoke(app, ["adhoc", path])

    mock_request.assert_called_once_with(path)
    assert result.exit_code == 0
    assert result.stdout == f"{return_value}\n"


def test_with_data(faker: Faker, mock_request: MagicMock) -> None:
    path = faker.pystr()
    data = faker.pydict(allowed_types=[str, float, int])
    return_value = faker.pystr()
    mock_request.return_value = return_value

    result = runner.invoke(app, ["adhoc", path, json.dumps(data)])

    mock_request.assert_called_once_with(path, data)
    assert result.exit_code == 0
    assert result.stdout == f"{return_value}\n"
