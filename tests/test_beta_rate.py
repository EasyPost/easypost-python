import pytest
from easypost.util import get_lowest_stateless_rate


@pytest.mark.vcr()
def test_beta_retrieve_stateless_rates(basic_shipment, test_client):
    """Tests that we can retrieve stateless rates when basic shipment data."""
    stateless_rates = test_client.beta_rate.retrieve_stateless_rates(**basic_shipment)

    assert all(rate["object"] == "Rate" for rate in stateless_rates)


@pytest.mark.vcr()
def test_beta_get_lowest_stateless_rate(basic_shipment, test_client):
    """Tests that we can return the lowest stateless rate from a list of stateless rates."""
    stateless_rates = test_client.beta_rate.retrieve_stateless_rates(**basic_shipment)

    lowest_stateless_rate = get_lowest_stateless_rate(stateless_rates)

    assert lowest_stateless_rate["service"] == "First"
