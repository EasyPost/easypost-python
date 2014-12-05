import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# create test tracker
tracker = easypost.Tracker.create(
    tracking_code="EZ2000000002",
    carrier="USPS"
)
print(tracker)

# retrieve tracker by id
tracker2 = easypost.Tracker.retrieve(tracker.id)

print(tracker2)
