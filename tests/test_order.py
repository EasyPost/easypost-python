import pytest

import easypost


@pytest.mark.vcr()
def test_order_create(basic_order):
    order = easypost.Order.create(**basic_order)

    assert isinstance(order, easypost.Order)
    assert str.startswith(order.id, "order_")
    assert order.rates is not None


@pytest.mark.vcr()
def test_order_retrieve(basic_order):
    order = easypost.Order.create(**basic_order)

    retrieved_order = easypost.Order.retrieve(order.id)

    assert isinstance(retrieved_order, easypost.Order)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert retrieved_order.id == order.id


@pytest.mark.vcr()
def test_order_get_rates(basic_order):
    order = easypost.Order.create(**basic_order)

    rates = order.get_rates()

    rates_array = rates["rates"]

    assert isinstance(rates_array, list)
    assert all(isinstance(rate, easypost.Rate) for rate in rates_array)


@pytest.mark.vcr()
def test_order_buy(usps, usps_service, basic_order):
    order = easypost.Order.create(**basic_order)
    order.buy(carrier=usps, service=usps_service)

    shipment_array = order["shipments"]

    assert all(shipment.postage_label is not None for shipment in shipment_array)


@pytest.mark.vcr()
def test_order_lowest_rate(basic_order):
    """Test various usage alterations of the lowest_rate method."""
    order = easypost.Order.create(**basic_order)

    # Test lowest rate with no filters
    lowest_rate = order.lowest_rate()
    assert lowest_rate.service == "First"
    assert lowest_rate.rate == "5.57"
    assert lowest_rate.carrier == "USPS"

    # Test lowest rate with service filter (this rate is higher than the lowest but should filter)
    lowest_rate_service = order.lowest_rate(services=["Priority"])
    assert lowest_rate_service.service == "Priority"
    assert lowest_rate_service.rate == "7.90"
    assert lowest_rate_service.carrier == "USPS"

    # Test lowest rate with carrier filter (should error due to bad carrier)
    with pytest.raises(easypost.Error) as error:
        order.lowest_rate(carriers=["BAD CARRIER"])
    assert str(error.value) == "No rates found."
