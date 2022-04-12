import pytest

import easypost


@pytest.mark.vcr()
def test_pickup_create(one_call_buy_shipment, basic_pickup):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = easypost.Pickup.create(**pickup_data)

    assert isinstance(pickup, easypost.Pickup)
    assert str.startswith(pickup.id, "pickup_")
    assert pickup.pickup_rates is not None


@pytest.mark.vcr()
def test_pickup_retrieve(one_call_buy_shipment, basic_pickup):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = easypost.Pickup.create(**pickup_data)

    retrieved_pickup = easypost.Pickup.retrieve(pickup.id)

    assert isinstance(retrieved_pickup, easypost.Pickup)
    assert retrieved_pickup == pickup


@pytest.mark.vcr()
def test_pickup_buy(usps, one_call_buy_shipment, basic_pickup, pickup_service):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = easypost.Pickup.create(**pickup_data)

    bought_pickup = pickup.buy(carrier=usps, service=pickup_service)

    assert isinstance(bought_pickup, easypost.Pickup)
    assert str.startswith(bought_pickup.id, "pickup_")
    assert bought_pickup.confirmation is not None
    assert bought_pickup.status == "scheduled"


@pytest.mark.vcr()
def test_pickup_cancel(usps, one_call_buy_shipment, basic_pickup, pickup_service):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    pickup_data = basic_pickup
    pickup_data["shipment"] = shipment

    pickup = easypost.Pickup.create(**pickup_data)

    bought_pickup = pickup.buy(carrier=usps, service=pickup_service)

    cancelled_pickup = bought_pickup.cancel()

    assert isinstance(cancelled_pickup, easypost.Pickup)
    assert str.startswith(cancelled_pickup.id, "pickup_")
    assert cancelled_pickup.status == "canceled"
