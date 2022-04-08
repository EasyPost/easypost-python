import pytest

import easypost


@pytest.mark.vcr()
def test_address_create(basic_address):
    address = easypost.Address.create(**basic_address)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "388 Townsend St"


@pytest.mark.vcr()
def test_address_create_verify_strict(basic_address):
    address_data = basic_address
    address_data["verify_strict"] = [True]

    address = easypost.Address.create(**address_data)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "388 TOWNSEND ST APT 20"


@pytest.mark.vcr()
def test_address_retrieve(basic_address):
    address = easypost.Address.create(**basic_address)

    retrieved_address = easypost.Address.retrieve(address.id)

    assert isinstance(retrieved_address, easypost.Address)
    assert retrieved_address == address


@pytest.mark.vcr()
def test_address_all(page_size):
    addresses = easypost.Address.all(page_size=page_size)

    addresses_array = addresses["addresses"]

    assert len(addresses_array) <= page_size
    assert addresses["has_more"] is not None
    assert all(isinstance(address, easypost.Address) for address in addresses_array)


@pytest.mark.vcr()
def test_address_create_verify(incorrect_address_to_verify):
    """Test creating a verified address.

    We purposefully pass in slightly incorrect data to get the corrected address back once verified.
    """
    incorrect_address_to_verify["verify"] = [True]

    address = easypost.Address.create(**incorrect_address_to_verify)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "417 MONTGOMERY ST FL 5"


@pytest.mark.vcr()
def test_address_create_and_verify(incorrect_address_to_verify):
    """Test creating a verified address.

    We purposefully pass in slightly incorrect data to get the corrected address back once verified.
    """
    incorrect_address_to_verify["verify"] = [True]

    address = easypost.Address.create_and_verify(**incorrect_address_to_verify)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "417 MONTGOMERY ST FL 5"


@pytest.mark.vcr()
def test_address_verify(basic_address):
    address = easypost.Address.create(**basic_address)
    address.verify()

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "388 Townsend St"
