import pytest

import easypost
from easypost.error import Error


@pytest.mark.vcr()
def test_scanform_create(one_call_buy_shipment):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    scanform = easypost.ScanForm.create(shipment=[shipment])

    assert isinstance(scanform, easypost.ScanForm)
    assert str.startswith(scanform.id, "sf_")


@pytest.mark.vcr()
def test_scanform_retrieve(one_call_buy_shipment):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    scanform = easypost.ScanForm.create(shipment=[shipment])

    retrieved_scanform = easypost.ScanForm.retrieve(scanform.id)

    assert isinstance(retrieved_scanform, easypost.ScanForm)
    assert retrieved_scanform == scanform


@pytest.mark.vcr()
def test_scanform_all(page_size):
    scanforms = easypost.ScanForm.all(page_size=page_size)

    scanforms_array = scanforms["scan_forms"]

    assert len(scanforms_array) <= page_size
    assert scanforms["has_more"] is not None
    assert all(isinstance(scanform, easypost.ScanForm) for scanform in scanforms_array)


@pytest.mark.vcr()
def test_scanform_get_next_page(page_size):
    try:
        scanforms = easypost.ScanForm.all(page_size=page_size)
        next_page = easypost.ScanForm.get_next_page(collection=scanforms, page_size=page_size)

        first_id_of_first_page = scanforms["scan_forms"][0].id
        first_id_of_second_page = next_page["scan_forms"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise Error(message="Test failed intentionally.")
