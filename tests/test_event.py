import inspect
import os
import time

import pytest

import easypost
from easypost.error import Error


@pytest.mark.vcr()
def test_event_all(page_size):
    events = easypost.Event.all(page_size=page_size)

    events_array = events["events"]

    assert len(events_array) <= page_size
    assert events["has_more"] is not None
    assert all(isinstance(event, easypost.Event) for event in events_array)


@pytest.mark.vcr()
def test_event_get_next_page(page_size):
    try:
        events = easypost.Event.all(page_size=page_size)
        next_page = easypost.Event.get_next_page(collection=events, page_size=page_size)

        first_id_of_first_page = events["events"][0].id
        first_id_of_second_page = next_page["events"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise Error(message="Test failed intentionally.")


@pytest.mark.vcr()
def test_event_retrieve(page_size):
    events = easypost.Event.all(page_size=page_size)

    event = events["events"][0]

    assert isinstance(event, easypost.Event)
    assert str.startswith(event.id, "evt_")


@pytest.mark.vcr()
def test_event_retrieve_all_payloads(page_size, webhook_url, one_call_buy_shipment):
    function_name = inspect.stack()[0][3]
    webhook = easypost.Webhook.create(url=webhook_url)

    easypost.Batch.create(shipments=[one_call_buy_shipment])

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(5)  # Wait enough time for the batch to process before getting events

    events = easypost.Event.all(page_size=page_size)
    payloads = easypost.Event.retrieve_all_payloads(events["events"][0]["id"])

    # Payloads may not be populated due to the webhook delivery system being on a queue
    assert all(isinstance(payload, easypost.Payload) for payload in payloads["payloads"])

    webhook.delete()  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_event_retrieve_payload(page_size, webhook_url, one_call_buy_shipment):
    function_name = inspect.stack()[0][3]
    webhook = easypost.Webhook.create(url=webhook_url)

    easypost.Batch.create(shipments=[one_call_buy_shipment])

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(5)  # Wait enough time for the batch to process before getting events

    events = easypost.Event.all(page_size=page_size)

    try:
        # Need a valid-length, invalid payload ID here
        easypost.Event.retrieve_payload(events["events"][0]["id"], "payload_11111111111111111111111111111111")
    except easypost.Error as error:
        assert error.message == "The payload(s) could not be found."
        assert error.http_status == 404

    webhook.delete()  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


def test_event_receive(event_json):
    event = easypost.Event.receive(event_json)

    assert isinstance(event, easypost.Event)
    assert str.startswith(event.id, "evt_")
