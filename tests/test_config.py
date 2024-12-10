from unittest.mock import MagicMock, patch

from faker import Faker

from alga import config


def test_get_sets_defaults(mock_config_file: MagicMock) -> None:
    mock_config_file.contents = {}

    cfg = config.get()

    assert cfg == {"version": 2, "tvs": {}}


def test_get_does_not_override_version(
    mock_config_file: MagicMock, faker: Faker
) -> None:
    version = faker.pyint()
    mock_config_file.contents = {"version": version}

    cfg = config.get()

    assert cfg == {"version": version, "tvs": {}}


def test_get_returns_data(mock_config_file: MagicMock, faker: Faker) -> None:
    data = {"version": faker.pyint(), "tvs": {}} | faker.pydict()
    mock_config_file.contents = data

    cfg = config.get()

    assert cfg == data


def test_get_calls_migrate(mock_config_file: MagicMock) -> None:
    mock_config_file.contents = {"version": 1}

    with patch("alga.config.migrate") as mock_migrate:
        config.get()

    mock_migrate.assert_called_once()


def test_write(mock_config_file: MagicMock, faker: Faker) -> None:
    data = faker.pydict()

    config.write(data)

    mock_config_file.write.assert_called_once()
    assert mock_config_file.contents == data


def test_migrate_v1_to_v2(faker: Faker) -> None:
    hostname, key, mac = faker.pystr(), faker.pystr(), faker.pystr()
    v1_config = {"version": 1, "hostname": hostname, "key": key, "mac": mac}

    assert config.migrate(v1_config) == {
        "version": 2,
        "default_tv": "default",
        "tvs": {"default": {"hostname": hostname, "key": key, "mac": mac}},
    }
