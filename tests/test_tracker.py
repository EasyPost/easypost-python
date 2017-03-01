# Unit tests related to 'Trackers' (https://www.easypost.com/docs/api#tracking).

import easypost


def test_tracker():
    # Create a tracker and then retrieve it. We assert on created and retrieved tracker's values.
    tracker = easypost.Tracker.create(
        tracking_code="EZ2000000002",
        carrier="USPS"
    )
    assert tracker.id                   # This is random

    # retrieve tracker by id
    tracker2 = easypost.Tracker.retrieve(tracker.id)

    assert tracker2.id == tracker.id                  # Should be the same as above

    # retrieve all trackers by tracking_code
    trackers = easypost.Tracker.all(tracking_code="EZ2000000002")

    assert len(trackers["trackers"])
    assert trackers["trackers"][0].id == tracker.id == tracker2.id   # Should be the same as the ids above

    # create another test tracker
    tracker3 = easypost.Tracker.create(
        tracking_code="EZ2000000002",
        carrier="USPS"
    )

    assert tracker3.id

    # retrieve all created since 'tracker'
    trackers2 = easypost.Tracker.all(after_id=tracker.id)

    assert len(trackers2["trackers"]) == 1             # Should be 1
    assert trackers2["has_more"] is False              # Should be false
    assert trackers2["trackers"][0].id == tracker3.id  # Should be the same as the id for tracker3
