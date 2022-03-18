import pytest

import easypost


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
