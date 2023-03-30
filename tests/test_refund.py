import pytest

import easypost
from easypost.error import Error


@pytest.mark.vcr()
def test_refund_create(one_call_buy_shipment, usps):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    # We need to retrieve the shipment so that the tracking_code has time to populate
    retrieved_shipment = easypost.Shipment.retrieve(shipment["id"])

    refund = easypost.Refund.create(
        carrier=usps,
        tracking_codes=[retrieved_shipment.tracking_code],
    )

    assert str.startswith(refund[0].id, "rfnd_")
    assert refund[0].status == "submitted"


@pytest.mark.vcr()
def test_refund_all(page_size):
    refunds = easypost.Refund.all(page_size=page_size)

    refunds_array = refunds["refunds"]

    assert len(refunds_array) <= page_size
    assert refunds["has_more"] is not None
    assert all(isinstance(refund, easypost.Refund) for refund in refunds_array)


@pytest.mark.vcr()
def test_refund_get_next_page(page_size):
    try:
        refunds = easypost.Refund.all(page_size=page_size)
        next_page = easypost.Refund.get_next_page(collection=refunds, page_size=page_size)

        first_id_of_first_page = refunds["refunds"][0].id
        first_id_of_second_page = next_page["refunds"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise Error(message="Test failed intentionally.")


@pytest.mark.vcr()
def test_refund_retrieve(page_size):
    refunds = easypost.Refund.all(page_size=page_size)

    retrieved_refund = easypost.Refund.retrieve(refunds["refunds"][0]["id"])

    assert isinstance(retrieved_refund, easypost.Refund)
    assert retrieved_refund.id == refunds["refunds"][0].id
