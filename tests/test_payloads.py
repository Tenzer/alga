from faker import Faker

from alga.payloads import get_hello_data


def test_get_hello_data(faker: Faker) -> None:
    client_key = faker.pystr()

    result = get_hello_data(client_key)

    assert isinstance(result, dict)
    assert result["payload"]["client-key"] == client_key


def test_get_hello_data_manifest_has_no_signature() -> None:
    result = get_hello_data()
    manifest = result["payload"]["manifest"]

    assert "signatures" not in manifest
    assert "signed" not in manifest
    assert "TEST_SECURE" in manifest["permissions"]
