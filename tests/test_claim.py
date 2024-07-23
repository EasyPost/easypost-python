import pytest
from easypost.constant import (
    _FILTERS_KEY,
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.models import (
    Claim,
    Shipment,
)


def _prepare_insured_shipment(client, shipment_data, claim_amount) -> Shipment:
    shipment = client.shipment.create(**shipment_data)
    rate = shipment.lowest_rate()
    purchased_shipment = client.shipment.buy(shipment.id, rate=rate)
    _ = client.shipment.insure(shipment.id, amount=claim_amount)

    return purchased_shipment


@pytest.mark.vcr()
def test_claim_create(full_shipment, basic_claim, test_client):
    claim_amount = "100.00"

    insured_shipment = _prepare_insured_shipment(test_client, full_shipment, claim_amount)

    claim_data = basic_claim
    claim_data["tracking_code"] = insured_shipment.tracking_code
    claim_data["amount"] = claim_amount

    claim = test_client.claim.create(**claim_data)

    assert isinstance(claim, Claim)
    assert str.startswith(claim.id, "clm_")
    assert claim.type == claim_data["type"]


@pytest.mark.vcr()
def test_claim_retrieve(full_shipment, basic_claim, test_client):
    claim_amount = "100.00"

    insured_shipment = _prepare_insured_shipment(test_client, full_shipment, claim_amount)

    claim_data = basic_claim
    claim_data["tracking_code"] = insured_shipment.tracking_code
    claim_data["amount"] = claim_amount

    claim = test_client.claim.create(**claim_data)

    retrieved_claim = test_client.claim.retrieve(claim.id)

    assert isinstance(retrieved_claim, Claim)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert claim.id == retrieved_claim.id


@pytest.mark.vcr()
def test_claim_all(page_size, test_client):
    claims = test_client.claim.all(page_size=page_size)

    claim_array = claims["claims"]

    assert len(claim_array) <= page_size
    assert claims["has_more"] is not None
    assert all(isinstance(claim, Claim) for claim in claim_array)


@pytest.mark.vcr()
def test_claim_get_next_page(page_size, test_client):
    try:
        first_page = test_client.claim.all(page_size=page_size)
        next_page = test_client.claim.get_next_page(claims=first_page, page_size=page_size)

        first_id_of_first_page = first_page["claims"][0].id
        first_id_of_second_page = next_page["claims"][0].id

        assert first_id_of_first_page != first_id_of_second_page

        # Verify that the filters are being passed along for behind-the-scenes reference
        assert first_page[_FILTERS_KEY] == next_page[_FILTERS_KEY]
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(_TEST_FAILED_INTENTIONALLY_ERROR)


@pytest.mark.vcr()
def test_claim_cancel(test_client, full_shipment, basic_claim):
    claim_amount = "100.00"

    insured_shipment = _prepare_insured_shipment(test_client, full_shipment, claim_amount)

    claim_data = basic_claim
    claim_data["tracking_code"] = insured_shipment.tracking_code
    claim_data["amount"] = claim_amount

    claim = test_client.claim.create(**claim_data)

    cancelled_claim = test_client.claim.cancel(id=claim.id)

    assert isinstance(cancelled_claim, Claim)
    assert str.startswith(cancelled_claim.id, "clm_")
    assert cancelled_claim.status == "cancelled"
