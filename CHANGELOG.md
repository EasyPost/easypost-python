# CHANGELOG

## v8.1.0 (2023-07-28)

- Adds new `RequestHook` and `ResponseHook` events. (un)subscribe to them with the new `subscribe_to_request_hook`, `subscribe_to_response_hook`, `unsubscribe_from_request_hook`, or `unsubscribe_from_response_hook` methods of an `EasyPostClient`
- Maps 400 status codes to new `BadRequestError` class

## v8.0.0 (2023-06-06)

See our [Upgrade Guide](UPGRADE_GUIDE.md#upgrading-from-7x-to-80) for more details.

- New `EasyPostClient` object
  - Logic is grouped together in Services and each EasyPost object has a new model (eg: `client.shipment.create()`)
- Error handling overhaul
  - Introduces ~2 dozen new error types that extend from either `ApiError` or `EasyPostError`
  - ApiErrors behave like the previous `Error` class did. They will include a `message`, `http_status`, and `http_body`. Additionally, a new `code` and `errors` keys are present and populate when available
- Beta namespace changed from `easypost.beta.x` to `client.beta_x`
- Empty API response functions return `None` instead of `True`
- Corrected naming conventions
  - References to `Referral` are now `ReferralCustomer` and `referral_customer` to match the API and docs
  - References to `Smartrate` are now `SmartRate` and `smart_rate` to match the API and docs
  - References to `Scanform` are now `ScanForm` and `scan_form`
  - `primary_or_secondary` paramater name for billing functions is now called `priority` to match the API and docs
- The `update_email` function of the `referral_customer` service had the parameter order switched so `id` (previously called `user_id`) is first which matches the rest of the library
- Retrieving carrier metadata is now in GA
- Dropped Python 3.6 support
- Bumps all dependencies

## v7.13.0 (2023-05-02)

- Adds `retrieve_estimated_delivery_date` function to the Shipment class

## v7.12.0 (2023-04-18)

- Adds beta `retrieve_carrier_metadata` function
- Improves error deserialization to handle bad format returned from the JSON

## v7.11.0 (2023-04-04)

- Adds `get_next_page` function that retrieves the next page of results for a paginated collection

## v7.10.0 (2023-02-17)

- Adds beta `retrieve_stateless_rates` function
- Adds `get_lowest_stateless_rate` function to filter the lowest stateless rate

## v7.9.0 (2023-01-18)

- Adds `all` function to `Pickup` to retrieve all pickups
- Adds `retrieve_payload` and `retrieve_all_payloads` functions to `Event`

## v7.8.0 (2023-01-11)

- Adds new beta billing functionality for ReferralCustomer users
  - `add_payment_method` can add a pre-existing Stripe bank account or credit card to your EasyPost account
  - `refund_by_amount` refunds your wallet by a dollar amount
  - `refund_by_payment_log` refunds you wallet by a PaymentLog ID

## v7.7.0 (2022-12-07)

- Routes requests for creating a carrier account with a custom workflow (eg: FedEx, UPS) to the correct endpoint when using the `create` function

## v7.6.1 (2022-10-24)

- Concatenates `error.message` if it incorrectly comes back from the API as a list

## v7.6.0 (2022-09-21)

- Adds support to pass `end_shipper_id` on the buy call of a Shipment
- Migrates the Partner White Label (Referral) functions from beta to the general library namespace and deprecates the beta functions

## v7.5.0 (2022-08-25)

- Adds the `EndShipper` class with `create`, `retrieve`, `all`, and `save` functions

## v7.4.0 (2022-08-02)

- Adds Carbon Offset support
  - Adds ability to create a shipment with carbon_offset
  - Adds ability to buy a shipment with carbon_offset
  - Adds ability to one-call-buy a shipment with carbon_offset
  - Adds ability to rerate a shipment with carbon_offset
- Adds `validate_webhook` function that returns your webhook or raises an error if there is a `webhook_secret` mismatch

## v7.3.0 (2022-07-18)

- Adds ability to generate forms for shipments via `generate_form()` function

## v7.2.0 (2022-07-11)

- Adds `Billing.retrieve_payment_methods()`, `Billing.fund_wallet()`, and `Billing.delete_payment_method()` functions
- Removes the unusable `carrier` param from `Address.verify()` along with the dead `message` conditional check that was missed in v7.0.0
- Adds OS specific details to the user-agent header
- API keys are now required for every request and will fail fast if not present
- Swaps update functions to use `patch` instead of `put` behind the scenes to better match the API behavior and documentation. Behavior of these functions should be unchanged

## v7.1.1 (2022-05-09)

- Fixes the inclusion of the new `beta` module

## v7.1.0 (2022-05-09)

- Adds a `lowest_rate()` function to Orders and Pickups
- Adds a `Shipment.get_lowest_smartrate()` function and a `shipment.lowest_smartrate()` function
- Adds beta Referral class for Partner White Label API with these new functions: `create()`, `update_email()`, `all()`, and `add_credit_card()`

## v7.0.0 (2022-04-14)

Upgrading major versions of this project? Refer to the [Upgrade Guide](UPGRADE_GUIDE.md).

### Breaking Changes

- Bumps minimum Python version from 2.7 to 3.6
- Bumps all dependencies
- Removes `shipment.get_rates()` method since the shipment object already has rates. If you need to get new rates for a shipment, please use the `shipment.regenerate_rates()` method.
- Removes `track_with_code` in shipment class since it's no longer being used
- Removes the unusable `carrier` param from `Address.create_and_verify()` along with the dead `message` conditional check
- Must pass a list object to `shipment.lowest_rate()` rather than a comma-separated list

### Features

- Adds the `update_brand()` method to the User object
- Adds Python version to user-agent header on requests
- Adds `retrieve_me()` convenience function that allow users to retrieve without specifying an ID.

### Chores

- Broke out the entire project into separate modules based on object
- Removes `_max_timeout` and instead uses a flat 60-second timeout for requests
- Added Makefile for much easier development management
- Added typehints throughout the project
- Consolidated all dependencies from various requirements files to `setup.py`
- Added a comprehensive test suite that tests all interfaces of the project
- Documented each interface of the project via docstrings

## v6.0.0 (2021-10-12)

Upgrading major versions of this project? Refer to the [Upgrade Guide](UPGRADE_GUIDE.md).

- JSON encodes POST bodies instead of form encoding them
- Adds support for `tax_identifiers`
- Black formatting and iSort tools added to repo
- Bumps `requests` from v1 to v2
- Various refactor efforts and code cleanup

## v5.1.3 (2021-07-20)

- Remove 2015-vintage experimental "`all_updated`" action from trackers
- Correct references of `contact@easypost.com` to `support@easypost.com`
- Clean up address verify property and some miscellaneous request logic

## vv5.1.2 (2021-06-10)

- Strips away the `result` key from SmartRate and simply returns an array of SmartRate objects

## v5.1.1 (2021-05-18)

- fix: stops appending smartrates to Shipment object

## v5.1.0 (2021-05-14)

- Adds `SmartRate` functionality to the `Shipments` object (available by calling `get_smartrates()` on a shipment)

## v5.0.0 (2020-08-10)

- Add `all` method for retrieving Events
- _[backwards-compatibility break]_ Remove `all` method for some un-supported types: CustomsItem, CustomsInfo, Pickup, and Order

## v4.1.0 (2020-05-11)

- change tests to use [vcrpy](https://github.com/kevin1024/vcrpy) so they are more reliable
- add `original_exception` to `easypost.Error` in cases where we are re-raising an underlying error (e.g., an HTTP exception)
- fix a bunch of flake8 warnings
- [potentially-breaking] soft-deprecate Python 3.3 and 3.4. these have been dropped by most of the libraries we use, so probably don't work anyway.
- Swap GET to POST on Refund method

## v4.0.2 (2020-05-05)

- cleaned up how the `__version__` attribute is populated to no longer throw warnings (#95, #98, #104)
- added some misding reports
- fix stale tests
- move testing infrastructure from travis-ci.org to travis-ci.com

## v4.0.1 (2020-03-06)

- Fixed a bug that would not create reports properly
- Fixed stale unit tests

## v4.0.0 (2019-07-09)

- Update some `setup.py` fields
- Formally remove Python 2.6 support (which has been broken for several years)

## v3.6.5 (2019-07-09)

- Fix broken pickup tests
- Fix broken reports tests
- Make tests run on Python 3.7
- Fix typo in `install_requires` causing `six` to not be installed by pip (gh-84 from @roehnan)

## v3.6.4 (2018-04-09)

**NOTE:** This version was never released

- Update user tests

## v3.6.3 (2018-02-05)

- Fix issue with responses that contain an `api_key` field (gh-67)
- Fix tests to take into account new label fee

## v3.6.2 (2017-05-23)

- Report.retrieve no longer requires a type to be passed

## v3.6.1 (2017-05-09)

- Modernize tests; make tests able to run in parallel; etc.
- Clarify in README and `setup.py` the supported Python versions
- Add top-level `timeout` variable for setting the HTTP timeout on requests

## v3.6.0 (2017-04-04)

- Changed Report CRUD signatures. requires report type to be passed

## v3.5.2 (2017-02-14)

- Added `get_rates` method to Order objects

## v3.5.1 (2017-01-19)

- Fixed create for ScanForms

## v3.5.0 (2017-01-18)

- Added basic CRUD methods for Webhook Objects
- Fixed Order test

## v3.4.0 (2016-12-20)

- Added session pooling

## v3.3.0 (2016-12-15)

- Added support for Report objects

## v3.2.2 (2016-07-29)

- Added support for Insurance objects

## v3.2.1 (2016-07-18)

- Added `to_json` method for EasyPost object. Thanks ThePsyjo!

## v3.2.0 (2016-05-17)

- Remove `api_keys` from object dumps
- Fixed address tests to keep them in line with the new API messages
- This was previously known as version 3.1.3

## v3.1.2 (2016-03-04)

- Added a suite of unittest tests. Thanks wyounas!

## v3.1.1 (2016-02-12)

- Added ability to interact with Users (create, retrieve and update)

## v3.1.0 (2015-12-08)

- Add verifications to Address.create

## v3.0.6 (2015-11-24)

- Added Blob.retrieve for fetching urls for blobs stored by EasyPost.

## v3.0.5 (2015-11-18)

- Changed the interface on `Tracker.create_list` to return True rather than the
  Trackers themselves

## v3.0.4 (2015-11-16)

- Minor bugfix

## v3.0.3 (2015-11-16)

- Added a `Tracker.all_updated` method for retrieving a large number of Trackers
  by status or `tracking_details` updated datetime

## v3.0.2 (2015-11-10)

- Added a `Tracker.create_list` method for creating a large number of Trackers
  at once

## v3.0.1 (2015-11-04)

- Fixed some examples and added some new ones, particularly dealing with Tracker.all

## v3.0.0 (2015-10-19)

- Fixed bug where retrieving a shipment by tracking code or reference doesn't set the ID properly

## v2.0.16 (2015-08-10)

- Added ability to interact with carrier accounts (full CRUD)

## v2.0.15 (2015-07-31)

- Fixed bug with address verification url rendering

## v2.0.14 (2015-03-30)

- Fix numerous bugs, including Python3 encoding

## v2.0.13 (2015-01-09)

- Added python3 support

## v2.0.12 (2014-11-04)

- Added tracker to shipment response
- Added tracker example

## v2.0.11 (2014-09-19)

- Added Order support.

## v2.0.10 (2014-09-10)

- Added Pickup cancellation method.

## v2.0.9 (2014-09-02)

- Added Pickup resource for scheduling pickups.

## v2.0.6 (2013-10-17)

- Added Event resource for webhook digestion.
- Added buy method to Batch.

## v2.0.5 (2013-09-22)

- Bug Fix: UTF-8 input handled more gracefully.

## v2.0.4 (2013-07-31)

- API Addition: Tracker resource added. Trackers can be used to register any tracking code with EasyPost webhooks.

## v2.0.3 (2013-07-23)

- API Addition: `Shipment.track_with_code` returns tracking details for any tracking code.

## v2.0.2 (2013-07-07)

- Bug fix: `address.create_and_verify` is now a classmethod.

## v2.0.1 (2013-07-05)

- Added function to Address to all creating and verifying at the same time.
- Add label function to Shipment to request specific label `file_formats` (pdf, epl2, zpl).
- Add insure function to Shipment. Add insurance to any shipment in one call!
- Fixed `shipment.get_rates` bug.
