from faker import Faker

from alga.types import App, Channel, InputDevice, SoundOutputDevice


def test_app(faker: Faker) -> None:
    id_, title = faker.pystr(), faker.pystr()
    app = App({"id": id_, "title": title})

    assert str(app) == f"{title} ({id_})"


def test_channel(faker: Faker) -> None:
    number, name = faker.pystr(), faker.pystr()
    channel = Channel(
        {"channelId": faker.pystr(), "channelNumber": number, "channelName": name}
    )

    assert str(channel) == f"{number}: {name}"


def test_input_device(faker: Faker) -> None:
    id_, name = faker.pystr(), faker.pystr()
    input_device = InputDevice({"id": id_, "label": name})

    assert str(input_device) == f"{name} ({id_})"


def test_sound_output_device(faker: Faker) -> None:
    name = faker.pystr()
    sound_output_device = SoundOutputDevice(faker.pystr(), name)

    assert str(sound_output_device) == name
