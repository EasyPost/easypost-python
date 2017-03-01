# Unit tests related to 'Order' (https://www.easypost.com/docs/api#orders).

import easypost


def test_order_create_then_buy():
    # We create an Order containing Shipment.
    # Towards the end we assert on Order and Parcel's values
    to_address = {
        'company': 'Oakland Dmv Office',
        'name': 'Customer',
        'street1': '5300 Claremont Ave',
        'city': 'Oakland',
        'state': 'CA',
        'zip': '94618',
        'country': 'US',
        'phone': '800-777-0133'
    }

    parcel1 = {
        'weight': 21.2,
        'length': 12,
        'width': 12,
        'height': 3
    }

    order = easypost.Order.create(
        to_address=to_address,
        from_address={
            'name': 'EasyPost',
            'company': 'EasyPost',
            'street1': '164 Townsend St',
            'city': 'San Francisco',
            'state': 'CA',
            'zip': '94107',
            'phone': '415-456-7890'
        },
        shipments=[{
            'parcel': parcel1,
            'options': {'label_format': 'PDF'}
        }, {
            'parcel': {
                'weight': 16,
                'length': 8,
                'width': 5,
                'height': 5
            },
            'options': {'label_format': 'PDF'}
        }]
    )

    rate_id = order.shipments[0].rates[0].id
    assert rate_id is not None

    order.get_rates()

    new_rate_id = order.shipments[0].rates[0].id
    assert new_rate_id is not None
    assert new_rate_id != rate_id

    assert order.buyer_address.name == to_address['name']
    assert order.buyer_address.company == to_address['company']
    assert order.buyer_address.street1 == to_address['street1']
    assert order.buyer_address.city == to_address['city']
    assert order.buyer_address.state == to_address['state']
    assert order.buyer_address.country == to_address['country']

    # Assert the shipment's parcel
    assert len(order.shipments) == 2

    square_box = [o.parcel for o in order.shipments if o.parcel.width == 5.0][0]
    long_box = [o.parcel for o in order.shipments if o.parcel.height == 3.0][0]

    assert long_box.height == parcel1['height']
    assert long_box.length == parcel1['length']
    assert long_box.width == parcel1['width']
    assert long_box.weight == parcel1['weight']
    assert square_box.height == 5.0
    assert square_box.length == 8.0
    assert square_box.width == 5.0
    assert square_box.weight == 16.0

    order.buy(carrier='USPS', service='Priority')

    for shipment in order.shipments:
        # Insure the parcel
        shipment.insure(amount=100)
        assert shipment.tracking_code
        assert shipment.insurance == '100.00'
        assert 'https://easypost-files.s3-us-west-2.amazonaws.com' in shipment.postage_label.label_url
