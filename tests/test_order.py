import pytest
from easypost.errors import FilteringError
from easypost.models import (
    Order,
    Rate,
)


@pytest.mark.vcr()
def test_order_create(basic_order, test_client):
    order = test_client.order.create(**basic_order)

    assert isinstance(order, Order)
    assert str.startswith(order.id, "order_")
    assert order.rates is not None


@pytest.mark.vcr()
def test_order_retrieve(basic_order, test_client):
    order = test_client.order.create(**basic_order)

    retrieved_order = test_client.order.retrieve(order.id)

    assert isinstance(retrieved_order, Order)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert retrieved_order.id == order.id


@pytest.mark.vcr()
def test_order_get_rates(basic_order, test_client):
    order = test_client.order.create(**basic_order)

    rates = test_client.order.get_rates(order.id)

    rates_array = rates["rates"]

    assert isinstance(rates_array, list)
    assert all(isinstance(rate, Rate) for rate in rates_array)


@pytest.mark.vcr()
def test_order_buy(usps, usps_service, basic_order, test_client):
    order = test_client.order.create(**basic_order)
    bought_order = test_client.order.buy(order.id, carrier=usps, service=usps_service)

    shipment_array = bought_order["shipments"]

    assert all(shipment.postage_label is not None for shipment in shipment_array)


@pytest.mark.vcr()
def test_order_lowest_rate(basic_order, test_client):
    """Test various usage alterations of the lowest_rate method."""
    order = test_client.order.create(**basic_order)

    # Test lowest rate with no filters
    lowest_rate = order.lowest_rate()
    assert lowest_rate.service == "First"
    assert lowest_rate.rate == "6.07"
    assert lowest_rate.carrier == "USPS"

    # Test lowest rate with service filter (this rate is higher than the lowest but should filter)
    lowest_rate_service = order.lowest_rate(services=["Priority"])
    assert lowest_rate_service.service == "Priority"
    assert lowest_rate_service.rate == "7.15"
    assert lowest_rate_service.carrier == "USPS"

    # Test lowest rate with carrier filter (should error due to bad carrier)
    with pytest.raises(FilteringError) as error:
        order.lowest_rate(carriers=["BAD CARRIER"])
    assert str(error.value) == "No rates found."
