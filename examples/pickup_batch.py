import time

import easypost

easypost.api_key = "API_KEY"

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
        "from_address": {
            "name": "Sawyer Bateman",
            "company": "EasyPost",
            "street1": "164 Townsend St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94107",
            "phone": "415-456-7890",
        },
        "parcel": {"weight": 21.2},
        "carrier": "UPS",
        "service": "NextDayAir",
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
        "parcel": {"weight": 21.2},
        "carrier": "UPS",
        "service": "NextDayAir",
    },
]

batch = easypost.Batch.create_and_buy(shipments=shipments)
while batch.state in ("creating", "queued_for_purchase", "purchasing"):
    print(batch.state)
    time.sleep(5)
    batch.refresh()

# Insure the shipments after purchase
if batch.state == "purchased":
    for shipment in batch.shipments:
        shipment.insure(amount=100)

pickup = easypost.Pickup.create(
    address={
        "name": "Sawyer Bateman",
        "company": "EasyPost",
        "street1": "164 Townsend St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94107",
        "phone": "415-456-7890",
    },
    batch=batch,
    reference="internal_id_1234",
    min_datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    max_datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),  # this should be later than min
    is_account_address=True,
    instructions="Special pickup instructions",
)
pickup.buy(carrier="UPS", service="Same-day Pickup")  # rates in pickup.pickup_rates

print(pickup.confirmation)
