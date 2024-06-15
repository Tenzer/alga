from unittest import mock

from faker import Faker

from alga import config


@mock.patch("alga.config._config_file")
def test_get_sets_version(mock_config_file: mock.MagicMock) -> None:
    mock_config_file.contents = {}

    cfg = config.get()

    assert cfg == {"version": 1}


@mock.patch("alga.config._config_file")
def test_get_does_not_override_version(
    mock_config_file: mock.MagicMock, faker: Faker
) -> None:
    version = faker.pyint()
    mock_config_file.contents = {"version": version}

    cfg = config.get()

    assert cfg == {"version": version}


@mock.patch("alga.config._config_file")
def test_get_returns_data(mock_config_file: mock.MagicMock, faker: Faker) -> None:
    data = {"version": faker.pyint()} | faker.pydict()
    mock_config_file.contents = data

    cfg = config.get()

    assert cfg == data


@mock.patch("alga.config._config_file")
def test_write(mock_config_file: mock.MagicMock, faker: Faker) -> None:
    data = faker.pydict()

    config.write(data)

    mock_config_file.write.assert_called_once()
    assert mock_config_file.contents == data
