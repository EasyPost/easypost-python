# Unit tests related to 'Batch' (https://www.easypost.com/docs/api#batches).

from time import sleep

import pytest

import easypost


@pytest.mark.vcr()
def test_batch_create_and_buy(vcr):
    # We create Address and Parcel objects. We then try to create a Batch containing a shipment.
    # Finally, we assert on saved and returned data.

    # from address and parcel don't change
    from_address = easypost.Address.create(
        name="Simpler Postage Inc.",
        street1="388 Townsend St",
        street2="Apt 20",
        city="San Francisco",
        state="CA",
        zip="94107",
        phone="415-456-7890",
    )

    parcel = easypost.Parcel.create(predefined_package="RegionalRateBoxA", weight=64)

    # # populate order_list from db, csv, etc.
    order_list = [
        {
            "address": {
                "name": "Jon Calhoun",
                "street1": "388 Townsend St",
                "street2": "Apt 30",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94107",
                "phone": "415-456-7890",
            },
            "order_number": "1234567890",
        }
    ]

    shipments = []

    for order in order_list:
        shipments.append(
            {
                "to_address": order["address"],
                "from_address": from_address,
                "parcel": parcel,
                "reference": order["order_number"],
                "carrier": "USPS",
                "service": "Priority",
            }
        )

    # create batch of shipments
    batch = easypost.Batch.create_and_buy(shipment=shipments)
    assert batch.num_shipments == 1

    # Poll while waiting for the batch to purchase the shipments
    while batch.state in ("creating", "queued_for_purchase", "purchasing"):
        if vcr.record_mode != "none":
            sleep(1)
        batch.refresh()

    # Insure the shipments after purchase
    if batch.state == "purchased":
        for shipment in batch.shipments:
            shipment.insure(amount=100)

    assert len(batch.shipments) == 1
    assert batch.shipments[0].batch_status == "postage_purchased"
    assert batch.shipments[0].buyer_address.city == "SAN FRANCISCO"
    assert batch.shipments[0].buyer_address.country == "US"
    assert batch.shipments[0].buyer_address.name == "JON CALHOUN"
    assert batch.shipments[0].buyer_address.phone == "4154567890"
    assert batch.shipments[0].buyer_address.street1 == "388 TOWNSEND ST APT 30"

    # Assert on fees
    assert batch.shipments[0].fees[0].amount == "0.00000"
    assert batch.shipments[0].fees[1].amount == "8.08000"
    assert batch.shipments[0].fees[2].amount == "0.50000"

    # Assert on parcel

    assert batch.shipments[0].parcel.predefined_package == "RegionalRateBoxA"
    assert batch.shipments[0].parcel.weight == 64.0

    # Assert on tracker
    assert batch.shipments[0].tracker.tracking_code and batch.shipments[0].tracker.shipment_id
