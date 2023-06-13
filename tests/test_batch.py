import inspect
import os
import time

import pytest
from easypost.models import Batch


@pytest.mark.vcr()
def test_batch_create(one_call_buy_shipment, test_client):
    batch = test_client.batch.create(shipments=[one_call_buy_shipment])

    assert isinstance(batch, Batch)
    assert str.startswith(batch.id, "batch_")
    assert batch.shipments is not None


@pytest.mark.vcr()
def test_batch_retrieve(one_call_buy_shipment, test_client):
    batch = test_client.batch.create(shipments=[one_call_buy_shipment])

    retrieved_batch = test_client.batch.retrieve(batch.id)

    assert isinstance(batch, Batch)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert retrieved_batch.id == batch.id


@pytest.mark.vcr()
def test_batch_all(page_size, test_client):
    batches = test_client.batch.all(page_size=page_size)

    batches_array = batches["batches"]

    assert len(batches_array) <= page_size
    assert batches["has_more"] is not None
    assert all(isinstance(batch, Batch) for batch in batches_array)


@pytest.mark.vcr()
def test_batch_create_and_buy(one_call_buy_shipment, test_client):
    batch = test_client.batch.create_and_buy(
        shipments=[
            one_call_buy_shipment,
            one_call_buy_shipment,
        ],
    )

    assert isinstance(batch, Batch)
    assert str.startswith(batch.id, "batch_")
    assert batch.num_shipments == 2


@pytest.mark.vcr()
def test_batch_buy(one_call_buy_shipment, test_client, synchronous_sleep_seconds):
    function_name = inspect.stack()[0][3]
    shipment_data = one_call_buy_shipment

    batch = test_client.batch.create(shipments=[shipment_data])

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(synchronous_sleep_seconds)  # Wait enough time for the batch to process before moving on

    bought_batch = test_client.batch.buy(batch.id)

    assert isinstance(bought_batch, Batch)
    assert bought_batch.num_shipments == 1


@pytest.mark.vcr()
def test_batch_create_scanform(one_call_buy_shipment, test_client, synchronous_sleep_seconds):
    function_name = inspect.stack()[0][3]
    shipment_data = one_call_buy_shipment

    batch = test_client.batch.create(shipments=[shipment_data])

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(synchronous_sleep_seconds)  # Wait enough time for the batch to process before moving on

    bought_batch = test_client.batch.buy(batch.id)

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(synchronous_sleep_seconds)  # Wait enough time for the batch to process before moving on

    batch_with_scanform = test_client.batch.create_scan_form(bought_batch.id)

    # We can't assert anything meaningful here because the scanform gets queued
    # for generation and may not be immediately available
    assert isinstance(batch_with_scanform, Batch)


@pytest.mark.vcr()
def test_batch_add_remove_shipment(one_call_buy_shipment, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    batch = test_client.batch.create()

    batch_with_shipments = test_client.batch.add_shipments(batch.id, shipments=[shipment])

    assert batch_with_shipments.num_shipments == 1

    batch_without_shipments = test_client.batch.remove_shipments(batch_with_shipments.id, shipments=[shipment])

    assert batch_without_shipments.num_shipments == 0


@pytest.mark.vcr()
def test_batch_label(one_call_buy_shipment, test_client, synchronous_sleep_seconds):
    function_name = inspect.stack()[0][3]

    batch = test_client.batch.create(shipments=[one_call_buy_shipment])

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(synchronous_sleep_seconds)  # Wait enough time for the batch to process before moving on

    bought_batch = test_client.batch.buy(batch.id)

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(synchronous_sleep_seconds)  # Wait enough time for the batch to process before moving on

    batch_with_label = test_client.batch.label(bought_batch.id, file_format="ZPL")

    # We can't assert anything meaningful here because the label gets queued
    # for generation and may not be immediately available
    assert isinstance(batch_with_label, Batch)
