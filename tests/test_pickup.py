# Unit tests related to 'Pickups' (https://www.easypost.com/docs/api#pickups).

import time
import unittest
import easypost
from constants import API_KEY as api_key
from time import gmtime, strftime

easypost.api_key = api_key


class PickupTests(unittest.TestCase):
    def test_pickup_batch(self):
        # Create a Batch containing multiple Shipments. Then we try to buy a Pickup and assert if it was bought.
        shipments = [
            {
                'to_address': {
                    'name': 'Customer',
                    'street1': '8308 Fenway Rd',
                    'city': 'Bethesda',
                    'state': 'MD',
                    'zip': '20817',
                    'country': 'US'
                },
                'from_address': {
                    'name': 'Sawyer Bateman',
                    'company': 'EasyPost',
                    'street1': '164 Townsend St',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'zip': '94107',
                    'phone': '415-456-7890'
                },
                'parcel': {
                    'weight': 10.2
                },
                'carrier': 'UPS',
                'service': 'NextDayAir'
            }, {
                'to_address': {
                    'name': 'Customer',
                    'street1': '8308 Fenway Rd',
                    'city': 'Bethesda',
                    'state': 'MD',
                    'zip': '20817',
                    'country': 'US'
                },
                'from_address': {
                    'name': 'Sawyer Bateman',
                    'company': 'EasyPost',
                    'street1': '164 Townsend St',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'zip': '94107',
                    'phone': '415-456-7890'
                },
                'parcel': {
                    'weight': 10.2
                },
                'carrier': 'UPS',
                'service': 'NextDayAir'
            }
        ]

        batch = easypost.Batch.create_and_buy(shipments=shipments)
        while batch.state in ('creating', 'queued_for_purchase', 'purchasing'):
            time.sleep(5)
            batch.refresh()

        # Insure the shipments after purchase
        if batch.state == 'purchased':
            for shipment in batch.shipments:
                shipment.insure(amount=100)

        pickup = easypost.Pickup.create(
            address={
                'name': 'Sawyer Bateman',
                'company': 'EasyPost',
                'street1': '164 Townsend St',
                'city': 'San Francisco',
                'state': 'CA',
                'zip': '94107',
                'phone': '415-456-7890'
            },
            batch=batch,
            reference='internal_id_1234',
            min_datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            max_datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),  # this should be later than min
            is_account_address=True,
            instructions='Special pickup instructions'
        )

        assert pickup.pickup_rates != []

        pickup.buy(
            carrier=pickup.pickup_rates[0].carrier,
            service=pickup.pickup_rates[0].service
        )

    def test_single_pickup(self):
        # Create a Shipment, buy it, and then buy a pickup for it
        shipment = easypost.Shipment.create(
            to_address={
                'name': 'Customer',
                'street1': '8308 Fenway Rd',
                'city': 'Bethesda',
                'state': 'MD',
                'zip': '20817',
                'country': 'US'
            },
            from_address={
                'name': 'Sawyer Bateman',
                'company': 'EasyPost',
                'street1': '164 Townsend St',
                'city': 'San Francisco',
                'state': 'CA',
                'zip': '94107',
                'phone': '415-456-7890'
            },
            parcel={
                'weight': 21.2
            }
        )

        shipment.buy(rate=shipment.lowest_rate('ups'), insurance=100.00)

        pickup = easypost.Pickup.create(
            address={
                'name': 'Sawyer Bateman',
                'company': 'EasyPost',
                'street1': '164 Townsend St',
                'city': 'San Francisco',
                'state': 'CA',
                'zip': '94107',
                'phone': '415-456-7890'
            },
            shipment=shipment,
            reference='internal_id_1234',
            min_datetime=strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            max_datetime=strftime('%Y-%m-%d %H:%M:%S', gmtime()),  # this should be later than min
            is_account_address=True,
            instructions='Special pickup instructions'
        )

        assert pickup.pickup_rates != []

        pickup.buy(
            carrier=pickup.pickup_rates[0].carrier,
            service=pickup.pickup_rates[0].service
        )
