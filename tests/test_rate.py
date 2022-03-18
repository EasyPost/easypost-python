import pytest

import easypost


@pytest.mark.vcr()
def test_rate_retrieve(basic_shipment):
    shipment = easypost.Shipment.create(**basic_shipment)

    rate = easypost.Rate.retrieve(shipment.rates[0].id)

    assert isinstance(rate, easypost.Rate)
    assert str.startswith(rate.id, "rate_")
