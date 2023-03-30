import pytest

import easypost
from easypost.error import Error


@pytest.mark.vcr()
def test_tracker_create():
    tracker = easypost.Tracker.create(tracking_code="EZ1000000001")

    assert isinstance(tracker, easypost.Tracker)
    assert str.startswith(tracker.id, "trk_")
    assert tracker.status == "pre_transit"


@pytest.mark.vcr()
def test_tracker_retrieve():
    tracker = easypost.Tracker.create(tracking_code="EZ1000000001")

    retrieved_tracker = easypost.Tracker.retrieve(tracker.id)

    assert isinstance(retrieved_tracker, easypost.Tracker)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert retrieved_tracker.id == tracker.id


@pytest.mark.vcr()
def test_tracker_all(page_size):
    trackers = easypost.Tracker.all(page_size=page_size)

    trackers_array = trackers["trackers"]

    assert len(trackers_array) <= page_size
    assert trackers["has_more"] is not None
    assert all(isinstance(tracker, easypost.Tracker) for tracker in trackers_array)


@pytest.mark.vcr()
def test_tracker_get_next_page(page_size):
    try:
        trackers = easypost.Tracker.all(page_size=page_size)
        next_page = easypost.Tracker.get_next_page(trackers=trackers, page_size=page_size)

        first_id_of_first_page = trackers["trackers"][0].id
        first_id_of_second_page = next_page["trackers"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise Error(message="Test failed intentionally.")


@pytest.mark.vcr()
def test_tracker_create_list():
    """Tests that we can create a list of trackers in bulk."""
    response = easypost.Tracker.create_list(
        {
            "0": {"tracking_code": "EZ1000000001"},
            "1": {"tracking_code": "EZ1000000002"},
            "2": {"tracking_code": "EZ1000000003"},
        }
    )

    # This endpoint/method does not return anything, just make sure the request doesn't fail
    assert response is True
