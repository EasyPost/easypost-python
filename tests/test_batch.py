# Unit tests related to 'Batch' (https://www.easypost.com/docs/api#batches).

import easypost

from time import sleep


def test_batch_create_and_buy():
    # We create Address and Parcel objects. We then try to create a Batch containing a shipment. Finally,
    # Finally, we assert on saved and returned data.

    # from address and parcel don't change
    from_address = easypost.Address.create(
        name='Simpler Postage Inc.',
        street1='388 Townsend St',
        street2='Apt 20',
        city='San Francisco',
        state='CA',
        zip='94107',
        phone='415-456-7890'
    )

    parcel = easypost.Parcel.create(
        predefined_package='RegionalRateBoxA',
        weight=64
    )

    # # populate order_list from db, csv, etc.
    order_list = [{
        'address': {
            'name': 'Jon Calhoun',
            'street1': '388 Townsend St',
            'street2': 'Apt 30',
            'city': 'San Francisco',
            'state': 'CA',
            'zip': '94107',
            'phone': '415-456-7890'
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
    assert batch.num_shipments == 1

    # Poll while waiting for the batch to purchase the shipments
    while batch.state in ('creating', 'queued_for_purchase', 'purchasing'):
        sleep(1)
        batch.refresh()

    # Insure the shipments after purchase
    if batch.state == 'purchased':
        for shipment in batch.shipments:
            shipment.insure(amount=100)

    assert len(batch.shipments) == 1
    assert batch.shipments[0].batch_status == 'postage_purchased'
    assert batch.shipments[0].buyer_address.city == 'San Francisco'
    assert batch.shipments[0].buyer_address.country == 'US'
    assert batch.shipments[0].buyer_address.name == 'Jon Calhoun'
    assert batch.shipments[0].buyer_address.phone == '4154567890'
    assert batch.shipments[0].buyer_address.street1 == '388 Townsend St'

    # Assert on fees
    assert batch.shipments[0].fees[0].amount == '0.01000'
    assert batch.shipments[0].fees[1].amount == '7.10000'
    assert batch.shipments[0].fees[2].amount == '1.00000'

    # Assert on parcel

    assert batch.shipments[0].parcel.predefined_package == 'RegionalRateBoxA'
    assert batch.shipments[0].parcel.weight == 64.0

    # Assert on tracker
    assert batch.shipments[0].tracker.tracking_code and batch.shipments[0].tracker.shipment_id
