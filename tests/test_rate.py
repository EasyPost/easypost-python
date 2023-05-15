import pytest

import easypost


@pytest.mark.vcr()
def test_rate_retrieve(basic_shipment, test_client):
    shipment = easypost.Shipment.create(**basic_shipment)  # TODO: Use new syntax once service exists

    rate = test_client.rate.retrieve(shipment.rates[0].id)

    assert isinstance(rate, easypost.Rate)
    assert str.startswith(rate.id, "rate_")
