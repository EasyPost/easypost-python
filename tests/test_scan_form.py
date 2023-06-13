import pytest
from easypost.constant import (
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.models import ScanForm


@pytest.mark.vcr()
def test_scanform_create(one_call_buy_shipment, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    scanform = test_client.scan_form.create(shipment=[shipment])

    assert isinstance(scanform, ScanForm)
    assert str.startswith(scanform.id, "sf_")


@pytest.mark.vcr()
def test_scanform_retrieve(one_call_buy_shipment, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    scanform = test_client.scan_form.create(shipment=[shipment])

    retrieved_scanform = test_client.scan_form.retrieve(scanform.id)

    assert isinstance(retrieved_scanform, ScanForm)
    assert retrieved_scanform == scanform


@pytest.mark.vcr()
def test_scanform_all(page_size, test_client):
    scanforms = test_client.scan_form.all(page_size=page_size)

    scanforms_array = scanforms["scan_forms"]

    assert len(scanforms_array) <= page_size
    assert scanforms["has_more"] is not None
    assert all(isinstance(scanform, ScanForm) for scanform in scanforms_array)


@pytest.mark.vcr()
def test_scanform_get_next_page(page_size, test_client):
    try:
        scanforms = test_client.scan_form.all(page_size=page_size)
        next_page = test_client.scan_form.get_next_page(scan_forms=scanforms, page_size=page_size)

        first_id_of_first_page = scanforms["scan_forms"][0].id
        first_id_of_second_page = next_page["scan_forms"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(message=_TEST_FAILED_INTENTIONALLY_ERROR)
