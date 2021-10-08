from time import gmtime, strftime

import easypost

easypost.api_key = "API_KEY"

shipment = easypost.Shipment.create(
    to_address={
        "name": "Customer",
        "street1": "8308 Fenway Rd",
        "city": "Bethesda",
        "state": "MD",
        "zip": "20817",
        "country": "US",
    },
    from_address={
        "name": "Sawyer Bateman",
        "company": "EasyPost",
        "street1": "164 Townsend St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94107",
        "phone": "415-456-7890",
    },
    parcel={"weight": 21.2},
)
print(shipment.rates)
# Purchase the postage label
shipment.buy(rate=shipment.lowest_rate("ups"))
# Insure the parcel
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
    shipment=shipment,
    reference="internal_id_1234",
    min_datetime=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
    max_datetime=strftime("%Y-%m-%d %H:%M:%S", gmtime()),  # this should be later than min
    is_account_address=True,
    instructions="Special pickup instructions",
)

pickup.buy(carrier="UPS", service="Same-day Pickup")  # rates in pickup.pickup_rates

print(pickup.confirmation)
print(pickup.status)

# pickup.cancel()
# print pickup.status
