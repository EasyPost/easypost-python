import pytest
from easypost.models import Rate


@pytest.mark.vcr()
def test_rate_retrieve(basic_shipment, test_client):
    shipment = test_client.shipment.create(**basic_shipment)

    rate = test_client.rate.retrieve(shipment.rates[0].id)

    assert isinstance(rate, Rate)
    assert str.startswith(rate.id, "rate_")
