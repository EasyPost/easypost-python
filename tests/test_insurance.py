import pytest

import easypost
from easypost.error import Error


@pytest.mark.vcr()
def test_insurance_create(one_call_buy_shipment, basic_insurance):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    insurance_data = basic_insurance
    insurance_data["tracking_code"] = shipment.tracking_code

    insurance = easypost.Insurance.create(**insurance_data)

    assert isinstance(insurance, easypost.Insurance)
    assert str.startswith(insurance.id, "ins_")
    assert insurance.amount == "100.00000"


@pytest.mark.vcr()
def test_insurance_retrieve(one_call_buy_shipment, basic_insurance):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    insurance_data = basic_insurance
    insurance_data["tracking_code"] = shipment.tracking_code

    insurance = easypost.Insurance.create(**insurance_data)

    retrieved_insurance = easypost.Insurance.retrieve(insurance.id)

    assert isinstance(retrieved_insurance, easypost.Insurance)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert insurance.id == retrieved_insurance.id


@pytest.mark.vcr()
def test_insurance_all(page_size):
    insurances = easypost.Insurance.all(page_size=page_size)

    insurance_array = insurances["insurances"]

    assert len(insurance_array) <= page_size
    assert insurances["has_more"] is not None
    assert all(isinstance(insurance, easypost.Insurance) for insurance in insurance_array)


@pytest.mark.vcr()
def test_insurance_get_next_page(page_size):
    try:
        insurances = easypost.Insurance.all(page_size=page_size)
        next_page = easypost.Insurance.get_next_page(collection=insurances, page_size=page_size)

        first_id_of_first_page = insurances["insurances"][0].id
        first_id_of_second_page = next_page["insurances"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise Error(message="Test failed intentionally.")
