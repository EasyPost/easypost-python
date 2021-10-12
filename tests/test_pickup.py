# Unit tests related to 'Pickups' (https://www.easypost.com/docs/api#pickups).

import datetime
import time

import pytest
import pytz

import easypost

ONE_DAY = datetime.timedelta(days=1)


@pytest.fixture
def noon_on_next_monday():
    today = datetime.date.today()
    next_monday = today + datetime.timedelta(days=(7 - today.weekday()))
    noon_est = datetime.time(12, 0, tzinfo=pytz.timezone("America/New_York"))
    return datetime.datetime.combine(next_monday, noon_est)


@pytest.mark.vcr()
def test_pickup_batch(noon_on_next_monday, vcr):
    # Create a Batch containing multiple Shipments. Then we try to buy a Pickup and assert if it was bought.

    pickup_address = easypost.Address.create(
        verify=["delivery"],
        name="TAKASHI KOVACS",
        company="EasyPost",
        street1="2889 W ASHTON BLVD",
        street2="SUITE 325",
        city="Lehi",
        state="UT",
        zip="84042",
        country="US",
        phone="415-456-7890",
    )

    shipments = [
        {
            "to_address": {
                "name": "Customer",
                "street1": "8308 Fenway Rd",
                "city": "Bethesda",
                "state": "MD",
                "zip": "20817",
                "country": "US",
            },
            "from_address": pickup_address,
            "parcel": {"weight": 10.2},
            "carrier": "USPS",
            "service": "Priority",
        },
        {
            "to_address": {
                "name": "Customer",
                "street1": "8308 Fenway Rd",
                "city": "Bethesda",
                "state": "MD",
                "zip": "20817",
                "country": "US",
            },
            "from_address": {
                "name": "Sawyer Bateman",
                "company": "EasyPost",
                "street1": "164 Townsend St",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94107",
                "phone": "415-456-7890",
            },
            "parcel": {"weight": 10.2},
            "carrier": "USPS",
            "service": "Priority",
        },
    ]

    batch = easypost.Batch.create_and_buy(shipments=shipments)
    while batch.state in ("creating", "queued_for_purchase", "purchasing"):
        if vcr.record_mode != "none":
            time.sleep(0.1)
        batch.refresh()

    # Insure the shipments after purchase
    if batch.state == "purchased":
        for shipment in batch.shipments:
            shipment.insure(amount=100)

    pickup = easypost.Pickup.create(
        address=pickup_address,
        batch=batch,
        reference="internal_id_1234",
        min_datetime=noon_on_next_monday.isoformat(),
        max_datetime=(noon_on_next_monday + ONE_DAY).isoformat(),
        is_account_address=True,
        instructions="Special pickup instructions",
    )

    assert pickup.pickup_rates != [], pickup.messages

    pickup.buy(carrier=pickup.pickup_rates[0].carrier, service=pickup.pickup_rates[0].service)


@pytest.mark.vcr()
def test_single_pickup(noon_on_next_monday):
    """Create a Shipment, buy it, and then buy a pickup for it"""

    pickup_address = easypost.Address.create(
        verify=["delivery"],
        name="TAKASHI KOVACS",
        company="EasyPost",
        street1="2889 W ASHTON BLVD",
        street2="SUITE 325",
        city="Lehi",
        state="UT",
        zip="84042",
        country="US",
        phone="415-456-7890",
    )

    shipment = easypost.Shipment.create(
        to_address={
            "name": "Customer",
            "street1": "8308 Fenway Rd",
            "city": "Bethesda",
            "state": "MD",
            "zip": "20817",
            "country": "US",
        },
        from_address=pickup_address,
        parcel={"weight": 21.2},
    )

    shipment.buy(rate=shipment.lowest_rate("USPS", "Priority"), insurance=100.00)

    pickup = easypost.Pickup.create(
        address=pickup_address,
        shipment=shipment,
        reference="internal_id_1234",
        min_datetime=noon_on_next_monday.isoformat(),
        max_datetime=(noon_on_next_monday + ONE_DAY).isoformat(),
        is_account_address=True,
        instructions="Special pickup instructions",
    )

    assert pickup.pickup_rates != [], pickup.messages

    pickup.buy(carrier=pickup.pickup_rates[0].carrier, service=pickup.pickup_rates[0].service)
