import inspect
import os
import time

import pytest

import easypost


@pytest.mark.vcr()
def test_batch_create(one_call_buy_shipment):
    batch = easypost.Batch.create(shipments=[one_call_buy_shipment])

    assert isinstance(batch, easypost.Batch)
    assert str.startswith(batch.id, "batch_")
    assert batch.shipments is not None


@pytest.mark.vcr()
def test_batch_retrieve(one_call_buy_shipment):
    batch = easypost.Batch.create(shipments=[one_call_buy_shipment])

    retrieved_batch = easypost.Batch.retrieve(batch.id)

    assert isinstance(batch, easypost.Batch)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert retrieved_batch.id == batch.id


@pytest.mark.vcr()
def test_batch_all(page_size):
    batches = easypost.Batch.all(page_size=page_size)

    batches_array = batches["batches"]

    assert len(batches_array) <= page_size
    assert batches["has_more"] is not None
    assert all(isinstance(batch, easypost.Batch) for batch in batches_array)


@pytest.mark.vcr()
def test_batch_create_and_buy(one_call_buy_shipment):
    batch = easypost.Batch.create_and_buy(
        shipments=[
            one_call_buy_shipment,
            one_call_buy_shipment,
        ],
    )

    assert isinstance(batch, easypost.Batch)
    assert str.startswith(batch.id, "batch_")
    assert batch.num_shipments == 2


@pytest.mark.vcr()
def test_batch_buy(one_call_buy_shipment):
    shipment_data = one_call_buy_shipment

    batch = easypost.Batch.create(shipments=[shipment_data])
    batch.buy()

    assert isinstance(batch, easypost.Batch)
    assert batch.num_shipments == 1


@pytest.mark.vcr()
def test_batch_create_scanform(one_call_buy_shipment):
    function_name = inspect.stack()[0][3]
    shipment_data = one_call_buy_shipment

    batch = easypost.Batch.create(shipments=[shipment_data])
    batch.buy()

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(5)  # Wait enough time for the batch to process before buying the shipment

    batch.create_scan_form()

    # We can't assert anything meaningful here because the scanform gets queued
    # for generation and may not be immediately available
    assert isinstance(batch, easypost.Batch)


@pytest.mark.vcr()
def test_batch_add_remove_shipment(one_call_buy_shipment):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    batch = easypost.Batch.create()

    batch.add_shipments(shipments=[shipment])

    assert batch.num_shipments == 1

    batch.remove_shipments(shipments=[shipment])

    assert batch.num_shipments == 0


@pytest.mark.vcr()
def test_batch_label(one_call_buy_shipment):
    function_name = inspect.stack()[0][3]

    batch = easypost.Batch.create(shipments=[one_call_buy_shipment])
    batch.buy()

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(5)  # Wait enough time for the batch to process before buying the shipment

    batch.label(file_format="ZPL")

    # We can't assert anything meaningful here because the label gets queued
    # for generation and may not be immediately available
    assert isinstance(batch, easypost.Batch)
