import pytest
from easypost.constant import (
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.models import Tracker


@pytest.mark.vcr()
def test_tracker_create(test_client):
    tracker = test_client.tracker.create(tracking_code="EZ1000000001")

    assert isinstance(tracker, Tracker)
    assert str.startswith(tracker.id, "trk_")
    assert tracker.status == "pre_transit"


@pytest.mark.vcr()
def test_tracker_retrieve(test_client):
    tracker = test_client.tracker.create(tracking_code="EZ1000000001")

    retrieved_tracker = test_client.tracker.retrieve(tracker.id)

    assert isinstance(retrieved_tracker, Tracker)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert retrieved_tracker.id == tracker.id


@pytest.mark.vcr()
def test_tracker_all(page_size, test_client):
    trackers = test_client.tracker.all(page_size=page_size)

    trackers_array = trackers["trackers"]

    assert len(trackers_array) <= page_size
    assert trackers["has_more"] is not None
    assert all(isinstance(tracker, Tracker) for tracker in trackers_array)


@pytest.mark.vcr()
def test_tracker_get_next_page(page_size, test_client):
    try:
        trackers = test_client.tracker.all(page_size=page_size)
        next_page = test_client.tracker.get_next_page(trackers=trackers, page_size=page_size)

        first_id_of_first_page = trackers["trackers"][0].id
        first_id_of_second_page = next_page["trackers"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(message=_TEST_FAILED_INTENTIONALLY_ERROR)


@pytest.mark.vcr()
def test_tracker_create_list(test_client):
    """Tests that we can create a list of trackers in bulk."""
    try:
        test_client.tracker.create_list(
            {
                "0": {"tracking_code": "EZ1000000001"},
                "1": {"tracking_code": "EZ1000000002"},
                "2": {"tracking_code": "EZ1000000003"},
            }
        )
    except Exception:
        assert False
