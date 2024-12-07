from faker import Faker

from alga.types import Channel, InputDevice


def test_channel(faker: Faker) -> None:
    channel = Channel(
        {
            "channelId": faker.pystr(),
            "channelNumber": faker.pystr(),
            "channelName": faker.pystr(),
        }
    )

    assert str(channel) == f"{channel.number}: {channel.name}"


def test_input_device(faker: Faker) -> None:
    input_device = InputDevice({"id": faker.pystr(), "label": faker.pystr()})

    assert str(input_device) == f"{input_device.name} ({input_device.id_})"
