from unittest.mock import MagicMock

from typer.testing import CliRunner

from alga.__main__ import app


runner = CliRunner()


def test_play(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["media", "play"])

    mock_request.assert_called_once_with("ssap://media.controls/play")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_pause(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["media", "pause"])

    mock_request.assert_called_once_with("ssap://media.controls/pause")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_stop(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["media", "stop"])

    mock_request.assert_called_once_with("ssap://media.controls/stop")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_fast_forward(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["media", "fast-forward"])

    mock_request.assert_called_once_with("ssap://media.controls/fastForward")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_rewind(mock_request: MagicMock) -> None:
    result = runner.invoke(app, ["media", "rewind"])

    mock_request.assert_called_once_with("ssap://media.controls/rewind")
    assert result.exit_code == 0
    assert result.stdout == ""
