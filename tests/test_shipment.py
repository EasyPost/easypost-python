# Unit tests related to 'Shipments' (https://www.easypost.com/docs/api#shipments).

import time

import easypost
import pytest


@pytest.mark.vcr()
def test_shipment_creation():
    # We create a shipment and assert on values saved.

    # create a to address and a from address
    to_address = easypost.Address.create(
        name='Sawyer Bateman',
        street1='1A Larkspur Cres.',
        street2='',
        city='St. Albert',
        state='AB',
        zip='t8n2m4',
        country='CA',
        phone='780-283-9384'
    )
    from_address = easypost.Address.create(
        company='EasyPost',
        street1='118 2nd St',
        street2='4th Fl',
        city='San Francisco',
        state='CA',
        zip='94105',
        phone='415-456-7890'
    )

    # create a parcel
    parcel = easypost.Parcel.create(
        length=10.2,
        width=7.8,
        height=4.3,
        weight=21.2
    )

    # create customs_info form for intl shipping
    customs_item = easypost.CustomsItem.create(
        description='EasyPost t-shirts',
        hs_tariff_number=123456,
        origin_country='US',
        quantity=2,
        value=96.27,
        weight=21.1
    )
    customs_info = easypost.CustomsInfo.create(
        customs_certify=1,
        customs_signer='Hector Hammerfall',
        contents_type='gift',
        contents_explanation='',
        eel_pfc='NOEEI 30.37(a)',
        non_delivery_option='return',
        restriction_type='none',
        restriction_comments='',
        customs_items=[customs_item]
    )

    # create shipment
    shipment = easypost.Shipment.create(
        to_address=to_address,
        from_address=from_address,
        parcel=parcel,
        customs_info=customs_info
    )

    rate_id = shipment.rates[0].id
    assert rate_id is not None

    # Assert address values match
    assert shipment.buyer_address.country == to_address.country
    assert shipment.buyer_address.phone == to_address.phone
    assert shipment.buyer_address.street1 == to_address.street1
    assert shipment.buyer_address.zip == to_address.zip
    assert shipment.customs_info.contents_explanation == customs_info.contents_explanation

    # Assert on parcel values match
    assert shipment.parcel.height == parcel.height
    assert shipment.parcel.weight == parcel.weight
    assert shipment.parcel.width == parcel.width

    # Assert customs items values match
    assert shipment.customs_info.customs_items[0].description == customs_item.description
    assert shipment.customs_info.customs_items[0].hs_tariff_number == customs_item.hs_tariff_number
    assert shipment.customs_info.customs_items[0].value == customs_item.value

    # buy shipment
    shipment.buy(rate=shipment.lowest_rate(['USPS', 'ups'], 'priorityMAILInternational'), insurance=100.00)

    # Assert shipment.buy set attributes correctly
    assert shipment.tracking_code is not None
    assert shipment.insurance == '100.00'

    assert 'https://easypost-files.s3-us-west-2.amazonaws.com' in shipment.postage_label.label_url


@pytest.mark.vcr()
@pytest.mark.slow
def test_rerate(vcr):
    # We create a shipment and assert on values saved.

    # create a to address and a from address
    to_address = easypost.Address.create(
        name='Sawyer Bateman',
        street1='1A Larkspur Cres.',
        street2='',
        city='St. Albert',
        state='AB',
        zip='t8n2m4',
        country='CA',
        phone='780-283-9384'
    )
    from_address = easypost.Address.create(
        company='EasyPost',
        street1='118 2nd St',
        street2='4th Fl',
        city='San Francisco',
        state='CA',
        zip='94105',
        phone='415-456-7890'
    )

    # create a parcel
    parcel = easypost.Parcel.create(
        length=10.2,
        width=7.8,
        height=4.3,
        weight=21.2
    )

    # create customs_info form for intl shipping
    customs_item = easypost.CustomsItem.create(
        description='EasyPost t-shirts',
        hs_tariff_number=123456,
        origin_country='US',
        quantity=2,
        value=96.27,
        weight=21.1
    )
    customs_info = easypost.CustomsInfo.create(
        customs_certify=1,
        customs_signer='Hector Hammerfall',
        contents_type='gift',
        contents_explanation='',
        eel_pfc='NOEEI 30.37(a)',
        non_delivery_option='return',
        restriction_type='none',
        restriction_comments='',
        customs_items=[customs_item]
    )

    # create shipment
    shipment = easypost.Shipment.create(
        to_address=to_address,
        from_address=from_address,
        parcel=parcel,
        customs_info=customs_info
    )

    rate_id = shipment.rates[0].id
    assert rate_id is not None

    if vcr.record_mode != 'none':
        # we only rerate on get_rates calls for shipments made at least 60 seconds ago
        time.sleep(61)

    easypost.requests_session.close()

    shipment.get_rates()

    new_rate_id = shipment.rates[0].id
    assert new_rate_id is not None
    assert new_rate_id != rate_id


@pytest.mark.vcr()
def test_smartrate(vcr):
    to_address = {
        'name': 'Dr. Steve Brule',
        'street1': '179 N Harbor Dr',
        'city': 'Redondo Beach',
        'state': 'CA',
        'zip': '90277',
        'country': 'US',
        'phone': '4153334444',
        'email': 'dr_steve_brule@gmail.com'
    }
    from_address = {
        'name': 'EasyPost',
        'street1': '417 Montgomery Street',
        'street2': '5th Floor',
        'city': 'San Francisco',
        'state': 'CA',
        'zip': '94104',
        'country': 'US',
        'phone': '4153334444',
        'email': 'support@easypost.com'
    }
    parcel = {
        'length': 20.2,
        'width': 10.9,
        'height': 5,
        'weight': 65.9
    }

    shipment = easypost.Shipment.create(
        to_address=to_address,
        from_address=from_address,
        parcel=parcel,
    )
    assert shipment.rates

    smartrates = shipment.get_smartrates()
    assert shipment.rates[0]['id'] == smartrates['result'][0]['id']
    assert smartrates['result'][0]['time_in_transit']['percentile_50'] == 1
    assert smartrates['result'][0]['time_in_transit']['percentile_75'] == 2
    assert smartrates['result'][0]['time_in_transit']['percentile_85'] == 2
    assert smartrates['result'][0]['time_in_transit']['percentile_90'] == 3
    assert smartrates['result'][0]['time_in_transit']['percentile_95'] == 3
    assert smartrates['result'][0]['time_in_transit']['percentile_97'] == 4
    assert smartrates['result'][0]['time_in_transit']['percentile_99'] == 5
