import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# create test tracker
tracker = easypost.Tracker.create(
    tracking_code="EZ2000000002",
    carrier="USPS"
)
print(tracker.id)                   # This is random

# retrieve tracker by id
tracker2 = easypost.Tracker.retrieve(tracker.id)

print(tracker2.id)                  # Should be the same as above

# retrieve all trackers by tracking_code
trackers = easypost.Tracker.all(tracking_code="EZ2000000002")

print(len(trackers["trackers"]))    # Should be 30
print(trackers["has_more"])         # Should be true, unless the len() isn't 30
print(trackers["trackers"][0].id)   # Should be the same as the ids above

# create another test tracker
tracker3 = easypost.Tracker.create(
    tracking_code="EZ2000000002",
    carrier="USPS"
)

print(tracker3.id)

# retrieve all created since 'tracker'
trackers2 = easypost.Tracker.all(after_id=tracker.id)

print(len(trackers2["trackers"]))   # Should be 1
print(trackers2["has_more"])        # Should be false
print(trackers2["trackers"][0].id)  # Should be the same as the id for tracker3
