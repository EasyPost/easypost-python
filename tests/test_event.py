import inspect
import os
import time

import pytest
from easypost.constant import (
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.errors import ApiError
from easypost.models import (
    Event,
    Payload,
)
from easypost.util import receive_event


@pytest.mark.vcr()
def test_event_all(page_size, test_client):
    events = test_client.event.all(page_size=page_size)

    events_array = events["events"]

    assert len(events_array) <= page_size
    assert events["has_more"] is not None
    assert all(isinstance(event, Event) for event in events_array)


@pytest.mark.vcr()
def test_event_get_next_page(page_size, test_client):
    try:
        events = test_client.event.all(page_size=page_size)
        next_page = test_client.event.get_next_page(events=events, page_size=page_size)

        first_id_of_first_page = events["events"][0].id
        first_id_of_second_page = next_page["events"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(message=_TEST_FAILED_INTENTIONALLY_ERROR)


@pytest.mark.vcr()
def test_event_retrieve(page_size, test_client):
    events = test_client.event.all(page_size=page_size)

    event = events["events"][0]

    assert isinstance(event, Event)
    assert str.startswith(event.id, "evt_")


@pytest.mark.vcr()
def test_event_retrieve_all_payloads(
    page_size, webhook_url, one_call_buy_shipment, synchronous_sleep_seconds, test_client
):
    function_name = inspect.stack()[0][3]
    webhook = test_client.webhook.create(url=webhook_url)

    test_client.batch.create(shipments=[one_call_buy_shipment])

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(synchronous_sleep_seconds)  # Wait enough time for the batch to process before getting events

    events = test_client.event.all(page_size=page_size)
    payloads = test_client.event.retrieve_all_payloads(events["events"][0]["id"])

    # Payloads may not be populated due to the webhook delivery system being on a queue
    assert all(isinstance(payload, Payload) for payload in payloads["payloads"])

    test_client.webhook.delete(
        webhook.id
    )  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_event_retrieve_payload(page_size, webhook_url, one_call_buy_shipment, synchronous_sleep_seconds, test_client):
    function_name = inspect.stack()[0][3]
    webhook = test_client.webhook.create(url=webhook_url)

    test_client.batch.create(shipments=[one_call_buy_shipment])

    if not os.path.exists(os.path.join("tests", "cassettes", f"{function_name}.yaml")):
        time.sleep(synchronous_sleep_seconds)  # Wait enough time for the batch to process before getting events

    events = test_client.event.all(page_size=page_size)

    try:
        # Need a valid-length, invalid payload ID here
        test_client.event.retrieve_payload(events["events"][0]["id"], "payload_11111111111111111111111111111111")
    except ApiError as error:
        assert error.message == "The payload(s) could not be found."
        assert error.http_status == 404

    test_client.webhook.delete(
        webhook.id
    )  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


def test_event_receive(event_json):
    event = receive_event(event_json)

    assert isinstance(event, Event)
    assert str.startswith(event.id, "evt_")
