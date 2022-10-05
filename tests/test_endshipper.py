import pytest

import easypost


@pytest.mark.vcr()
def test_endshipper_create(ca_address_1):
    endshipper = easypost.EndShipper.create(**ca_address_1)

    assert isinstance(endshipper, easypost.EndShipper)
    assert str.startswith(endshipper.id, "es_")
    assert endshipper.street1 == "388 TOWNSEND ST APT 20"


@pytest.mark.vcr()
def test_endshipper_retrieve(ca_address_1):
    endshipper = easypost.EndShipper.create(**ca_address_1)

    retrieved_endshipper = easypost.EndShipper.retrieve(endshipper.id)

    assert isinstance(retrieved_endshipper, easypost.EndShipper)
    assert endshipper.street1 == retrieved_endshipper.street1


@pytest.mark.vcr()
def test_endshipper_all(page_size):
    endshippers = easypost.EndShipper.all(page_size=page_size)

    endshipper_array = endshippers["end_shippers"]

    assert len(endshipper_array) <= page_size
    assert all(isinstance(endshipper, easypost.EndShipper) for endshipper in endshipper_array)


@pytest.mark.vcr()
def test_endshipper_update(ca_address_1):
    endshipper = easypost.EndShipper.create(**ca_address_1)

    endshipper.name = "Captain Sparrow"
    endshipper.company = "EasyPost"
    endshipper.street1 = "388 Townsend St"
    endshipper.street2 = "Apt 20"
    endshipper.city = "San Francisco"
    endshipper.state = "CA"
    endshipper.zip = "94107"
    endshipper.country = "US"
    endshipper.phone = "9999999999"
    endshipper.email = "test@example.com"
    endshipper = endshipper.save()

    assert isinstance(endshipper, easypost.EndShipper)
    assert str.startswith(endshipper.id, "es")
    assert endshipper.name == "CAPTAIN SPARROW"  # Name is capitalized becasue API will autocapitalize response
