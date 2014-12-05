import easypost
import time

easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

shipments = [
    {
        'to_address': {
            'name': "Customer",
            'street1': "8308 Fenway Rd",
            'city': "Bethesda",
            'state': "MD",
            'zip': "20817",
            'country': "US"
        },
        'from_address': {
            'name': "Sawyer Bateman",
            'company': "EasyPost",
            'street1': "164 Townsend St",
            'city': "San Francisco",
            'state': "CA",
            'zip': "94107",
            'phone': "415-456-7890"
        },
        'parcel': {
            'weight': 21.2
        },
        'carrier': "UPS",
        'service': "NextDayAir"
    }, {
        'to_address': {
            'name': "Customer",
            'street1': "8308 Fenway Rd",
            'city': "Bethesda",
            'state': "MD",
            'zip': "20817",
            'country': "US"
        },
        'from_address': {
            'name': "Sawyer Bateman",
            'company': "EasyPost",
            'street1': "164 Townsend St",
            'city': "San Francisco",
            'state': "CA",
            'zip': "94107",
            'phone': "415-456-7890"
        },
        'parcel': {
            'weight': 21.2
        },
        'carrier': "UPS",
        'service': "NextDayAir"
    }
]

batch = easypost.Batch.create(shipments = shipments)
while batch.state != 'created':
    time.sleep(5)
    batch.refresh()

pickup = easypost.Pickup.create(
    address = {
        'name': "Sawyer Bateman",
        'company': "EasyPost",
        'street1': "164 Townsend St",
        'city': "San Francisco",
        'state': "CA",
        'zip': "94107",
        'phone': "415-456-7890"
    },
    batch = batch,
    reference = "internal_id_1234",
    min_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    max_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), # this should be later than min
    is_account_address = True,
    instructions = "Special pickup instructions"
)
pickup.buy(carrier = "UPS", service = "Same-day Pickup") # rates in pickup.pickup_rates

print(pickup.confirmation)
