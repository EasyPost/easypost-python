# Unit tests related to 'ScanForms' (https://www.easypost.com/docs/api.html#manifesting-scan-form).

import easypost


def test_scan_form_create_and_retrieve():
    # prepare params for shipment
    to_address = {
        "name": "Sawyer Bateman",
        "street1": "1A Larkspur Cres.",
        "street2": "",
        "city": "St. Albert",
        "state": "AB",
        "zip": "t8n2m4",
        "country": "CA",
        "phone": "780-283-9384"
    }
    from_address = {
        "company": "EasyPost",
        "street1": "118 2nd St",
        "street2": "4th Fl",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94105",
        "phone": "415-456-7890"
    }
    parcel = {
        "length": 10.2,
        "width": 7.8,
        "height": 4.3,
        "weight": 21.2
    }
    customs_item = {
        "description": "EasyPost t-shirts",
        "hs_tariff_number": 123456,
        "origin_country": "US",
        "quantity": 2,
        "value": 96.27,
        "weight": 21.1
    }
    customs_info = {
        "customs_certify": 1,
        "customs_signer": "Hector Hammerfall",
        "contents_type": "gift",
        "contents_explanation": "",
        "eel_pfc": "NOEEI 30.37(a)",
        "non_delivery_option": "return",
        "restriction_type": "none",
        "restriction_comments": "",
        "customs_items": [customs_item]
    }

    # create shipment and buy
    shipment = easypost.Shipment.create(
        to_address=to_address,
        from_address=from_address,
        parcel=parcel,
        customs_info=customs_info
    )
    shipment.buy(rate=shipment.lowest_rate(['USPS', 'ups'], 'priorityMAILInternational'), insurance=100.00)

    # create scan form
    scan_form = easypost.ScanForm.create(
        shipments=[shipment]
    )

    # Assert values match
    assert scan_form.id is not None
    assert scan_form.tracking_codes[0] == shipment.tracking_code

    # retrieve a copy of the scan form
    scan_form2 = easypost.ScanForm.retrieve(scan_form.id)

    # Assert values match
    assert scan_form2.id == scan_form.id

    # index scan_forms
    scan_forms = easypost.ScanForm.all(page_size=2)

    assert len(scan_forms['scan_forms']) > 0
