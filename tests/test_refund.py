import pytest
from easypost.constant import (
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.models import Refund


@pytest.mark.vcr()
def test_refund_create(one_call_buy_shipment, usps, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    # We need to retrieve the shipment so that the tracking_code has time to populate
    retrieved_shipment = test_client.shipment.retrieve(shipment["id"])

    refund = test_client.refund.create(
        carrier=usps,
        tracking_codes=[retrieved_shipment.tracking_code],
    )

    assert str.startswith(refund[0].id, "rfnd_")
    assert refund[0].status == "submitted"


@pytest.mark.vcr()
def test_refund_all(page_size, test_client):
    refunds = test_client.refund.all(page_size=page_size)

    refunds_array = refunds["refunds"]

    assert len(refunds_array) <= page_size
    assert refunds["has_more"] is not None
    assert all(isinstance(refund, Refund) for refund in refunds_array)


@pytest.mark.vcr()
def test_refund_get_next_page(page_size, test_client):
    try:
        refunds = test_client.refund.all(page_size=page_size)
        next_page = test_client.refund.get_next_page(refunds=refunds, page_size=page_size)

        first_id_of_first_page = refunds["refunds"][0].id
        first_id_of_second_page = next_page["refunds"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(message=_TEST_FAILED_INTENTIONALLY_ERROR)


@pytest.mark.vcr()
def test_refund_retrieve(page_size, test_client):
    refunds = test_client.refund.all(page_size=page_size)

    retrieved_refund = test_client.refund.retrieve(refunds["refunds"][0]["id"])

    assert isinstance(retrieved_refund, Refund)
    assert retrieved_refund.id == refunds["refunds"][0].id
