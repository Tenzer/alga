from faker import Faker

from alga.payloads import get_hello_data


def test_get_hello_data(faker: Faker) -> None:
    client_key = faker.pystr()

    result = get_hello_data(client_key)

    assert isinstance(result, dict)
    assert result["payload"]["client-key"] == client_key
