import pytest

import easypost


@pytest.mark.vcr()
def test_event_all(page_size):
    events = easypost.Event.all(page_size=page_size)

    events_array = events["events"]

    assert len(events_array) <= page_size
    assert events["has_more"] is not None
    assert all(isinstance(event, easypost.Event) for event in events_array)


@pytest.mark.vcr()
def test_event_retrieve(page_size):
    events = easypost.Event.all(page_size=page_size)

    event = events["events"][0]

    assert isinstance(event, easypost.Event)
    assert str.startswith(event.id, "evt_")


@pytest.mark.vcr()
def test_event_retrieve_payloads(page_size, webhook_url, one_call_buy_shipment):
    webhook = easypost.Webhook.create(url=webhook_url)

    easypost.Batch.create(shipments=[one_call_buy_shipment])

    events = easypost.Event.all(page_size=page_size)
    payloads = easypost.Event.retrieve_payloads(events["events"][0]["id"])

    # Payloads may not be populated due to the webhook delivery system being on a queue
    assert all(isinstance(payload, easypost.Payload) for payload in payloads["payloads"])

    webhook.delete()  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_event_retrieve_payload(page_size, webhook_url, one_call_buy_shipment):
    webhook = easypost.Webhook.create(url=webhook_url)

    easypost.Batch.create(shipments=[one_call_buy_shipment])

    events = easypost.Event.all(page_size=page_size)

    with pytest.raises(Exception) as error:
        # Need a valid-length, invalid payload ID here
        easypost.Event.retrieve_payload(events["events"][0]["id"], "payload_11111111111111111111111111111111")

    assert str(error.value) == "The payload(s) could not be found."

    webhook.delete()  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


def test_event_receive(event_json):
    event = easypost.Event.receive(event_json)

    assert isinstance(event, easypost.Event)
    assert str.startswith(event.id, "evt_")
