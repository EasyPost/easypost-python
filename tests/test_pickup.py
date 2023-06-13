import pytest
from easypost.constant import (
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.errors import FilteringError
from easypost.models import Pickup


@pytest.mark.vcr()
def test_pickup_create(one_call_buy_shipment, basic_pickup, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = test_client.pickup.create(**pickup_data)

    assert isinstance(pickup, Pickup)
    assert str.startswith(pickup.id, "pickup_")
    assert pickup.pickup_rates is not None


@pytest.mark.vcr()
def test_pickup_all(page_size, test_client):
    pickups = test_client.pickup.all(page_size=page_size)

    pickup_array = pickups["pickups"]

    assert len(pickup_array) <= page_size
    assert pickups["has_more"] is not None
    assert all(isinstance(pickup, Pickup) for pickup in pickup_array)


@pytest.mark.vcr()
def test_pickup_get_next_page(page_size, test_client):
    try:
        pickups = test_client.pickup.all(page_size=page_size)
        next_page = test_client.pickup.get_next_page(pickups=pickups, page_size=page_size)

        first_id_of_first_page = pickups["pickups"][0].id
        first_id_of_second_page = next_page["pickups"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(message=_TEST_FAILED_INTENTIONALLY_ERROR)


@pytest.mark.vcr()
def test_pickup_retrieve(one_call_buy_shipment, basic_pickup, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = test_client.pickup.create(**pickup_data)

    retrieved_pickup = test_client.pickup.retrieve(pickup.id)

    assert isinstance(retrieved_pickup, Pickup)
    assert retrieved_pickup == pickup


@pytest.mark.vcr()
def test_pickup_buy(usps, one_call_buy_shipment, basic_pickup, pickup_service, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = test_client.pickup.create(**pickup_data)

    bought_pickup = test_client.pickup.buy(pickup.id, carrier=usps, service=pickup_service)

    assert isinstance(bought_pickup, Pickup)
    assert str.startswith(bought_pickup.id, "pickup_")
    assert bought_pickup.confirmation is not None
    assert bought_pickup.status == "scheduled"


@pytest.mark.vcr()
def test_pickup_cancel(usps, one_call_buy_shipment, basic_pickup, pickup_service, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = test_client.pickup.create(**pickup_data)

    bought_pickup = test_client.pickup.buy(pickup.id, carrier=usps, service=pickup_service)

    cancelled_pickup = test_client.pickup.cancel(bought_pickup.id)

    assert isinstance(cancelled_pickup, Pickup)
    assert str.startswith(cancelled_pickup.id, "pickup_")
    assert cancelled_pickup.status == "canceled"


@pytest.mark.vcr()
def test_pickup_lowest_rate(one_call_buy_shipment, basic_pickup, test_client):
    """Test various usage alterations of the lowest_rate method."""
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = test_client.pickup.create(**pickup_data)

    # Test lowest rate with no filters
    lowest_rate = pickup.lowest_rate()
    assert lowest_rate.service == "NextDay"
    assert lowest_rate.rate == "0.00"
    assert lowest_rate.carrier == "USPS"

    # Test lowest rate with service filter (should error due to bad service)
    with pytest.raises(FilteringError) as error:
        pickup.lowest_rate(services=["BAD SERVICE"])
    assert str(error.value) == "No rates found."

    # Test lowest rate with carrier filter (should error due to bad carrier)
    with pytest.raises(FilteringError) as error:
        pickup.lowest_rate(carriers=["BAD CARRIER"])
    assert str(error.value) == "No rates found."
