import json
from unittest.mock import MagicMock, call, patch

from faker import Faker
from typer.testing import CliRunner

from alga.__main__ import app
from alga.types import App


runner = CliRunner()


def test_current(faker: Faker, mock_request: MagicMock) -> None:
    app_id = faker.pystr()
    mock_request.return_value = {"appId": app_id}

    result = runner.invoke(app, ["app", "current"])

    mock_request.assert_called_once_with(
        "ssap://com.webos.applicationManager/getForegroundAppInfo"
    )
    assert result.exit_code == 0
    assert result.stdout == f"The current app is {app_id}\n"


def test_close(faker: Faker, mock_request: MagicMock) -> None:
    app_id = faker.pystr()

    result = runner.invoke(app, ["app", "close", app_id])

    mock_request.assert_called_once_with("ssap://system.launcher/close", {"id": app_id})
    assert result.exit_code == 0
    assert result.stdout == ""


def test_launch_without_data(faker: Faker, mock_request: MagicMock) -> None:
    app_id = faker.pystr()

    result = runner.invoke(app, ["app", "launch", app_id])

    mock_request.assert_called_once_with(
        "ssap://system.launcher/launch", {"id": app_id}
    )
    assert result.exit_code == 0
    assert result.stdout == ""


def test_launch_with_data(faker: Faker, mock_request: MagicMock) -> None:
    app_id = faker.pystr()
    data = faker.pydict()

    result = runner.invoke(app, ["app", "launch", app_id, json.dumps(data)])

    mock_request.assert_called_once_with(
        "ssap://system.launcher/launch", {"id": app_id} | data
    )
    assert result.exit_code == 0
    assert result.stdout == ""


def test_list(faker: Faker, mock_request: MagicMock) -> None:
    return_value = {
        "apps": [
            {"id": faker.pystr(), "title": faker.pystr()},
            {"id": faker.pystr(), "title": faker.pystr()},
            {"id": faker.pystr(), "title": faker.pystr()},
        ]
    }
    mock_request.return_value = return_value

    result = runner.invoke(app, ["app", "list"])

    mock_request.assert_called_once_with("ssap://com.webos.applicationManager/listApps")
    assert result.exit_code == 0

    splitted_output = result.stdout.split("\n")
    assert len(splitted_output) == (
        3  # table header
        + 3  # apps
        + 1  # table footer
        + 1  # trailing newline
    )
    assert splitted_output[3:6] == sorted(splitted_output[3:6])


def test_info(faker: Faker, mock_request: MagicMock) -> None:
    app_id = faker.pystr()
    app_info = faker.pystr()
    mock_request.return_value = {"appInfo": app_info}

    result = runner.invoke(app, ["app", "info", app_id])

    mock_request.assert_called_once_with(
        "ssap://com.webos.applicationManager/getAppInfo", {"id": app_id}
    )
    assert result.exit_code == 0
    assert result.stdout == f"{app_info}\n"


def test_pick(faker: Faker, mock_request: MagicMock) -> None:
    return_value = {
        "apps": [
            {"id": faker.pystr(), "title": faker.pystr()},
            {"id": faker.pystr(), "title": faker.pystr()},
            {"id": faker.pystr(), "title": faker.pystr()},
        ]
    }
    mock_request.return_value = return_value
    first_app = return_value["apps"][0]

    with patch("alga.cli_app.pzp") as mock_pzp:
        mock_pzp.return_value = App(first_app)

        result = runner.invoke(app, ["app", "pick"])

    mock_request.assert_has_calls(
        [
            call("ssap://com.webos.applicationManager/listApps"),
            call("ssap://system.launcher/launch", {"id": first_app["id"]}),
        ]
    )
    assert result.exit_code == 0
