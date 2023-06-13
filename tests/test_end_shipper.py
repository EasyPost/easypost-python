import pytest
from easypost.models import EndShipper


@pytest.mark.vcr()
def test_endshipper_create(ca_address_1, test_client):
    endshipper = test_client.end_shipper.create(**ca_address_1)

    assert isinstance(endshipper, EndShipper)
    assert str.startswith(endshipper.id, "es_")
    assert endshipper.street1 == "388 TOWNSEND ST APT 20"


@pytest.mark.vcr()
def test_endshipper_retrieve(ca_address_1, test_client):
    endshipper = test_client.end_shipper.create(**ca_address_1)

    retrieved_endshipper = test_client.end_shipper.retrieve(endshipper.id)

    assert isinstance(retrieved_endshipper, EndShipper)
    assert endshipper.street1 == retrieved_endshipper.street1


@pytest.mark.vcr()
def test_endshipper_all(page_size, test_client):
    endshippers = test_client.end_shipper.all(page_size=page_size)

    endshipper_array = endshippers["end_shippers"]

    assert len(endshipper_array) <= page_size
    assert all(isinstance(endshipper, EndShipper) for endshipper in endshipper_array)


@pytest.mark.vcr()
def test_endshipper_update(ca_address_1, test_client):
    endshipper = test_client.end_shipper.create(**ca_address_1)

    updated_endshipper = test_client.end_shipper.update(
        endshipper.id,
        name="Captain Sparrow",
        company="EasyPost",
        street1="388 Townsend St",
        street2="Apt 20",
        city="San Francisco",
        state="CA",
        zip="94107",
        country="US",
        phone="9999999999",
        email="test@example.com",
    )

    assert isinstance(updated_endshipper, EndShipper)
    assert str.startswith(updated_endshipper.id, "es")
    assert updated_endshipper.name == "CAPTAIN SPARROW"  # Name is capitalized becasue API will autocapitalize response
