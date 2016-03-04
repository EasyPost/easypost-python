# Unit tests related to 'Order' (https://www.easypost.com/docs/api#orders).

import unittest
import easypost
from constants import API_KEY as api_key

easypost.api_key = api_key


class OrderTests(unittest.TestCase):

    def test_order_create_then_buy(self):
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

        assert order.buyer_address.name == to_address['name']
        assert order.buyer_address.company == to_address['company']
        assert order.buyer_address.street1 == to_address['street1']
        assert order.buyer_address.city == to_address['city']
        assert order.buyer_address.state == to_address['state']
        assert order.buyer_address.country == to_address['country']

        # Assert the shipment's parcel
        assert len(order.shipments) == 2
        assert order.shipments[1].parcel.height == parcel1['height']
        assert order.shipments[1].parcel.width == parcel1['width']
        assert order.shipments[1].parcel.weight == parcel1['weight']

        order.buy(carrier='USPS', service='Priority')

        for shipment in order.shipments:
            # Insure the parcel
            shipment.insure(amount=100)
            assert shipment.tracking_code
            assert shipment.insurance == '100.00'
            assert 'http://assets.geteasypost.com' in shipment.postage_label.label_url


if __name__ == '__main__':
    unittest.main()
