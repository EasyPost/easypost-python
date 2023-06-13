import pytest
from easypost.constant import (
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.models import Insurance


@pytest.mark.vcr()
def test_insurance_create(one_call_buy_shipment, basic_insurance, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    insurance_data = basic_insurance
    insurance_data["tracking_code"] = shipment.tracking_code

    insurance = test_client.insurance.create(**insurance_data)

    assert isinstance(insurance, Insurance)
    assert str.startswith(insurance.id, "ins_")
    assert insurance.amount == "100.00000"


@pytest.mark.vcr()
def test_insurance_retrieve(one_call_buy_shipment, basic_insurance, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    insurance_data = basic_insurance
    insurance_data["tracking_code"] = shipment.tracking_code

    insurance = test_client.insurance.create(**insurance_data)

    retrieved_insurance = test_client.insurance.retrieve(insurance.id)

    assert isinstance(retrieved_insurance, Insurance)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert insurance.id == retrieved_insurance.id


@pytest.mark.vcr()
def test_insurance_all(page_size, test_client):
    insurances = test_client.insurance.all(page_size=page_size)

    insurance_array = insurances["insurances"]

    assert len(insurance_array) <= page_size
    assert insurances["has_more"] is not None
    assert all(isinstance(insurance, Insurance) for insurance in insurance_array)


@pytest.mark.vcr()
def test_insurance_get_next_page(page_size, test_client):
    try:
        insurances = test_client.insurance.all(page_size=page_size)
        next_page = test_client.insurance.get_next_page(insurances=insurances, page_size=page_size)

        first_id_of_first_page = insurances["insurances"][0].id
        first_id_of_second_page = next_page["insurances"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(message=_TEST_FAILED_INTENTIONALLY_ERROR)
