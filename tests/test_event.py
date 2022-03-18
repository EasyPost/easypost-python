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
def test_event_receive(event):
    event = easypost.Event.receive(event)

    assert isinstance(event, easypost.Event)
    assert str.startswith(event.id, "evt_")
