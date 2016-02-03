"""
Unit tests around the 'Shipment' endpoint (https://www.easypost.com/docs/api#shipments)
"""
import unittest
import easypost
from constants import API_KEY as api_key


class ShipmentTests(unittest.TestCase):

    def test_shipment_creation(self):
        """
        We create a shipment and assert on values saved.
        :return:
        """
        to_address = easypost.Address.create(
            api_key,
            name="Sawyer Bateman",
            street1="1A Larkspur Cres.",
            street2="",
            city="St. Albert",
            state="AB",
            zip="t8n2m4",
            country="CA",
            phone="780-283-9384"
        )
        from_address = easypost.Address.create(
            api_key,
            company="EasyPost",
            street1="118 2nd St",
            street2="4th Fl",
            city="San Francisco",
            state="CA",
            zip="94105",
            phone="415-456-7890"
        )

        # verify address
        verified_from_address = from_address.verify()

        parcel = easypost.Parcel.create(
            api_key,
            length=10.2,
            width=7.8,
            height=4.3,
            weight=21.2
            )
        # create customs_info form for intl shipping
        customs_item = easypost.CustomsItem.create(
            api_key,
            description="EasyPost t-shirts",
            hs_tariff_number=123456,
            origin_country="US",
            quantity=2,
            value=96.27,
            weight=21.1
        )
        customs_info = easypost.CustomsInfo.create(
            api_key,
            customs_certify=1,
            customs_signer="Hector Hammerfall",
            contents_type="gift",
            contents_explanation="",
            eel_pfc="NOEEI 30.37(a)",
            non_delivery_option="return",
            restriction_type="none",
            restriction_comments="",
            customs_items=[customs_item]
        )

        # create shipment
        shipment = easypost.Shipment.create(
            api_key,
            to_address=to_address,
            from_address=verified_from_address,
            parcel=parcel,
            customs_info=customs_info
        )
        assert shipment.buyer_address.country == to_address.country
        assert shipment.buyer_address.phone == to_address.phone
        assert shipment.buyer_address.street1 == to_address.street1
        assert shipment.buyer_address.zip == to_address.zip
        assert shipment.customs_info.contents_explanation == customs_info.contents_explanation
        # Assert customs items
        assert shipment.customs_info.customs_items[0].description == customs_item.description
        assert shipment.customs_info.customs_items[0].hs_tariff_number == customs_item.hs_tariff_number
        assert shipment.customs_info.customs_items[0].value == customs_item.value

        # Assert on shipment's parcel
        assert shipment.parcel.height == parcel.height
        assert shipment.parcel.weight == parcel.weight
        assert shipment.parcel.width == parcel.width

        shipment.buy(rate=shipment.lowest_rate(
            ['USPS', 'ups'], 'priorityMAILInternational'))
        # Insure the shipment for the value
        shipment.insure(amount=100)

        # shipment.refund()
        # print(shipment.refund_status)

        assert shipment.tracking_code
        assert shipment.insurance == '100.00'
        assert 'http://assets.geteasypost.com' in shipment.postage_label.label_url

