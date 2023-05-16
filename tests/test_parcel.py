import pytest

import easypost


@pytest.mark.vcr()
def test_parcel_create(basic_parcel, test_client):
    parcel = test_client.parcel.create(**basic_parcel)

    assert isinstance(parcel, easypost.Parcel)
    assert str.startswith(parcel.id, "prcl_")
    assert parcel.weight == 15.4


@pytest.mark.vcr()
def test_parcel_retrieve(basic_parcel, test_client):
    parcel = test_client.parcel.create(**basic_parcel)

    retrieved_parcel = test_client.parcel.retrieve(parcel.id)

    assert isinstance(retrieved_parcel, easypost.Parcel)
    assert retrieved_parcel == parcel
