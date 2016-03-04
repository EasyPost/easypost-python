from time import sleep

import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'
# easypost.api_base = 'http://localhost:5000/v2'

# from address and parcel don't change
from_address = easypost.Address.create(
    name="Simpler Postage Inc.",
    street1="388 Townsend St",
    street2="Apt 20",
    city="San Francisco",
    state="CA",
    zip="94107",
    phone="415-456-7890"
)

parcel = easypost.Parcel.create(
    predefined_package="RegionalRateBoxA",
    weight=64
)

# # populate order_list from db, csv, etc.
order_list = [{
    'address': {
        'name': "Jon Calhoun",
        'street1': "388 Townsend St",
        'street2': "Apt 30",
        'city': "San Francisco",
        'state': "CA",
        'zip': "94107",
        'phone': "415-456-7890"
    },
    'order_number': '1234567890'
}]

shipments = []

for order in order_list:
    shipments.append({
        'to_address': order['address'],
        'from_address': from_address,
        'parcel': parcel,
        'reference': order['order_number'],
        'carrier': 'USPS',
        'service': 'Priority'
    })

# create batch of shipments
batch = easypost.Batch.create_and_buy(shipment=shipments)

# Poll while waiting for the batch to purchase the shipments
while batch.state in ("creating", "queued_for_purchase", "purchasing"):
    sleep(5)
    batch.refresh()
    print(batch.state)

# Insure the shipments after purchase
if batch.state == "purchased":
    for shipment in batch.shipments:
        shipment.insure(amount=100)

###### below here should probably be in a seperate script so that there's no risk of re-running create_and_buy

# # run this to check on the batch status after it's been created
# # postage is purchased asyncronously, so you'll have to poll until it's done
# batch = easypost.Batch.retrieve('batch_DUvMxu2I')

# # by default batch.shipments only contain the shipment_id and batch_status/batch_message
# # expand any shipment details you'd like to see like this
# batch.shipments[0].refresh()


# # once all shipments are in 'postage_purchased' status you can generate a label file
# if batch.status.created == 0 and batch.status.postage_purchase_failed == 0 and not batch.label_url:
#   batch.label(file_format = 'pdf')


# # generating a label is also asyncronous, so you'll have to retrieve the batch object again
# # later to look for the batch.label_url!
# batch = easypost.Batch.retrieve('batch_XXXXXXXX')

print(batch)
