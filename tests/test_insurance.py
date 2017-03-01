# Unit tests related to 'Shipments' (https://www.easypost.com/docs/api#shipments).

import easypost


def test_insurance_creation():
    # We create an insurance and assert on values saved.
    tracking_code = "EZ2000000002"
    carrier = "USPS"
    amount = 101.00

    to_address = {
        "name": "Dr. Steve Brule",
        "street1": "179 N Harbor Dr",
        "city": "Redondo Beach",
        "state": "CA",
        "zip": "90277",
        "phone": "310-808-5243"
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

    # create insurance
    insurance = easypost.Insurance.create(
        to_address=to_address,
        from_address=from_address,
        tracking_code=tracking_code,
        carrier=carrier,
        amount=amount
    )

    # Assertions that create worked as expected
    assert isinstance(insurance.to_address, easypost.Address)
    assert isinstance(insurance.from_address, easypost.Address)
    assert insurance.tracking_code == tracking_code
    assert insurance.amount == "101.00000"
    assert isinstance(insurance.tracker, easypost.Tracker)

    insurance2 = easypost.Insurance.retrieve(insurance.id)

    # Assertions that retrieve worked as expected
    assert insurance2.id == insurance.id
    assert isinstance(insurance2.to_address, easypost.Address)
    assert isinstance(insurance2.from_address, easypost.Address)
    assert insurance2.tracking_code == tracking_code
    assert insurance2.amount == "101.00000"
    assert isinstance(insurance2.tracker, easypost.Tracker)

    insurances = easypost.Insurance.all(page_size=5)

    # Assertions that index worked as expected
    assert len(insurances["insurances"]) == 5
    assert insurances["has_more"]
