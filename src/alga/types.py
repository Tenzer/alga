from dataclasses import dataclass
from typing import Any


@dataclass
class App:
    id_: str
    name: str

    def __init__(self, app: dict[str, Any]) -> None:
        self.id_ = app["id"]
        self.name = app["title"]

    def __str__(self) -> str:
        return f"{self.name} ({self.id_})"


@dataclass
class Channel:
    id_: str
    number: str
    name: str

    def __init__(self, channel: dict[str, Any]) -> None:
        self.id_ = channel["channelId"]
        self.number = channel["channelNumber"]
        self.name = channel["channelName"]

    def __str__(self) -> str:
        return f"{self.number}: {self.name}"


@dataclass
class InputDevice:
    id_: str
    name: str

    def __init__(self, input_device: dict[str, Any]) -> None:
        self.id_ = input_device["id"]
        self.name = input_device["label"]

    def __str__(self) -> str:
        return f"{self.name} ({self.id_})"


@dataclass
class SoundOutputDevice:
    id_: str
    name: str

    def __str__(self) -> str:
        return self.name
