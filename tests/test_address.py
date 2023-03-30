import pytest

import easypost
from easypost.error import Error


@pytest.mark.vcr()
def test_address_create(ca_address_1):
    address = easypost.Address.create(**ca_address_1)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "388 Townsend St"


@pytest.mark.vcr()
def test_address_create_verify(incorrect_address):
    """Test creating an address with the verify param.

    We purposefully pass in slightly incorrect data to get the corrected address back once verified.
    """
    incorrect_address["verify"] = True

    address = easypost.Address.create(**incorrect_address)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "417 MONTGOMERY ST FL 5"


@pytest.mark.vcr()
def test_address_create_verify_strict(ca_address_1):
    """Test creating an address with the verify_strict param.

    We purposefully pass in slightly incorrect data to get the corrected address back once verified.
    """
    address_data = ca_address_1
    address_data["verify_strict"] = True

    address = easypost.Address.create(**address_data)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "388 TOWNSEND ST APT 20"


@pytest.mark.vcr()
def test_address_create_verify_array(incorrect_address):
    """Test creating an address with the verify param as an array.

    We purposefully pass in slightly incorrect data to get the corrected address back once verified.
    """
    incorrect_address["verify"] = [True]

    address = easypost.Address.create(**incorrect_address)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "417 MONTGOMERY ST FL 5"


@pytest.mark.vcr()
def test_address_create_and_verify(ca_address_1):
    address = easypost.Address.create_and_verify(**ca_address_1)

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "388 TOWNSEND ST APT 20"


@pytest.mark.vcr()
def test_address_retrieve(ca_address_1):
    address = easypost.Address.create(**ca_address_1)

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
def test_address_get_next_page(page_size):
    try:
        addresses = easypost.Address.all(page_size=page_size)
        next_page = easypost.Address.get_next_page(collection=addresses, page_size=page_size)

        first_id_of_first_page = addresses["addresses"][0].id
        first_id_of_second_page = next_page["addresses"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise Error(message="Test failed intentionally.")


@pytest.mark.vcr()
def test_address_verify(ca_address_1):
    """Test verifying an already created address."""
    address = easypost.Address.create(**ca_address_1)
    address.verify()

    assert isinstance(address, easypost.Address)
    assert str.startswith(address.id, "adr_")
    assert address.street1 == "388 Townsend St"


@pytest.mark.vcr()
def test_address_verify_invalid_address():
    """Test verifying an already created address."""
    with pytest.raises(easypost.Error) as error:
        address = easypost.Address.create(
            street1="invalid",
        )
        address.verify()

    assert str(error.value) == "Unable to verify address."
