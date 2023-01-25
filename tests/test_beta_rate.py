import pytest

import easypost


@pytest.mark.vcr()
def test_retrieve_stateless_rates(basic_shipment):
    response = easypost.beta.Rate.retrieve_stateless_rates(**basic_shipment)

    stateless_rates = response["rates"]

    assert all(rate["object"] == "Rate" for rate in stateless_rates)
