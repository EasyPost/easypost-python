### NEXT (unreleased)

### 3.6.3 2018-02-05

* Fix issue with responses that contain an `api_key` field (gh-67)
* Fix tests to take into account new label fee

### 3.6.2 2017-05-23

* Report.retrieve no longer requires a type to be passed

### 3.6.1 2017-05-09

* Modernize tests; make tests able to run in parallel; etc.
* Clarify in README and `setup.py` the supported Python versions
* Add top-level `timeout` variable for setting the HTTP timeout on requests

### 3.6.0 2017-04-04

* Changed Report CRUD signatures. requires report type to be passed

### 3.5.2 2017-02-14

* Added `get_rates` method to Order objects


### 3.5.1 2017-01-19

* Fixed create for ScanForms


### 3.5.0 2017-01-18

* Added basic CRUD methods for Webhook Objects
* Fixed Order test


### 3.4.0 2016-12-20

* Added session pooling


### 3.3.0 2016-12-15

* Added support for Report objects


### 3.2.2 2016-07-29

* Added support for Insurance objects


### 3.2.1 2016-07-18

* Added `to_json` method for EasyPost object. Thanks ThePsyjo!


### 3.2.0 2016-05-17

* Remove `api_keys` from object dumps
* Fixed address tests to keep them in line with the new API messages
* This was previously known as version 3.1.3


### 3.1.2 2016-03-04

* Added a suite of unittest tests. Thanks wyounas!


### 3.1.1 2016-02-12

* Added ability to interact with Users (create, retrieve and update)


### 3.1.0 2015-12-08

* Add verifications to Address.create


### 3.0.6 2015-11-24

* Added Blob.retrieve for fetching urls for blobs stored by EasyPost.


### 3.0.5 2015-11-18

* Changed the interface on `Tracker.create_list` to return True rather than the
Trackers themselves


### 3.0.4 2015-11-16

* Minor bugfix


### 3.0.3 2015-11-16

* Added a `Tracker.all_updated` method for retrieving a large number of Trackers
by status or `tracking_details` updated datetime


### 3.0.2 2015-11-10

* Added a `Tracker.create_list` method for creating a large number of Trackers
at once


### 3.0.1 2015-11-04

* Fixed some examples and added some new ones, particularly dealing with Tracker.all


### 3.0.0 2015-10-19

* Fixed bug where retrieving a shipment by tracking code or reference doesn't set the ID properly


### 2.0.16 2015-08-10

* Added ability to interact with carrier accounts (full CRUD)


### 2.0.15 2015-07-31

* Fixed bug with address verification url rendering

### 2.0.14 2015-03-30

* Fix numerous bugs, including Python3 encoding


### 2.0.13 2015-01-09

* Added python3 support


### 2.0.12 2014-11-04

* Added tracker to shipment response
* Added tracker example


### 2.0.11 2014-09-19

* Added Order support.


### 2.0.10 2014-09-10

* Added Pickup cancellation method.


### 2.0.9 2014-09-02

* Added Pickup resource for scheduling pickups.


### 2.0.6 2013-10-17

* Added Event resource for webhook digestion.
* Added buy method to Batch.


### 2.0.5 2013-09-22

* Bug Fix: UTF-8 input handled more gracefully.


### 2.0.4 2013-07-31

* API Addition: Tracker resource added. Trackers can be used to register any tracking code with EasyPost webhooks.


### 2.0.3 2013-07-23

* API Addition: `Shipment.track_with_code` returns tracking details for any tracking code.


### 2.0.2 2013-07-07

* Bug fix: `address.create_and_verify` is now a classmethod.


### 2.0.1 2013-07-05

* Added function to Address to all creating and verifying at the same time.
* Add label function to Shipment to request specific label `file_formats` (pdf, epl2, zpl).
* Add insure function to Shipment. Add insurance to any shipment in one call!
* Fixed `shipment.get_rates` bug.
