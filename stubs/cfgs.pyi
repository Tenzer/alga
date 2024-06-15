from typing import Any

class App:
    config: Directory

    def __init__(self, name: str, format: str = ...) -> None: ...

class Directory:
    def __init__(self, home: str, dirs: str, format: str) -> None: ...
    def open(self, filename: str | None = None) -> File: ...

class File:
    contents: dict[str, Any]
    def write(self) -> None: ...
