from typing import Any

from cfgs import App


_config_file = App("alga").config.open("config.json")


def get() -> dict[str, Any]:
    config = _config_file.contents
    config.setdefault("version", 1)
    return config


def write(config: dict[str, Any]) -> None:
    _config_file.contents = config
    _config_file.write()
