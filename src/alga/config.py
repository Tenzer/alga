from typing import Any

from cfgs import App


_config_file = App("alga").config.open("config.json")
_latest_version = 2


def get() -> dict[str, Any]:
    config = _config_file.contents

    if config.setdefault("version", _latest_version) < _latest_version:
        config = migrate(config)
        write(config)

    config.setdefault("tvs", {})

    return config


def migrate(config: dict[str, Any]) -> dict[str, Any]:
    if config["version"] == 1:
        config = {
            "version": 2,
            "default_tv": "default",
            "tvs": {
                "default": {
                    "hostname": config["hostname"],
                    "key": config["key"],
                    "mac": config["mac"],
                }
            },
        }

    return config


def write(config: dict[str, Any]) -> None:
    _config_file.contents = config
    _config_file.write()
