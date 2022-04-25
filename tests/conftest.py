import json
import os

import pytest

import easypost


EASYPOST_TEST_API_KEY = os.environ["EASYPOST_TEST_API_KEY"]
EASYPOST_PROD_API_KEY = os.environ["EASYPOST_PROD_API_KEY"]


def pytest_sessionstart(session):
    # this is for local unit testing with google appengine, otherwise you get a
    # 'No api proxy found for service "urlfetch"' response
    try:
        from google.appengine.ext import testbed  # type: ignore

        session.appengine_testbed = testbed.Testbed()  # type: ignore
        session.appengine_testbed.activate()  # type: ignore
        session.appengine_testbed.init_urlfetch_stub()  # type: ignore
    except ImportError:
        # if the import fails then we're not using the appengine sdk, so just
        # keep going without initializing the testbed stub
        pass


def pytest_sessionfinish(session, exitstatus):
    if hasattr(session, "appengine_testbed"):
        session.appengine_testbed.deactivate()  # type: ignore


# this fixture is auto-loaded by all tests; it sets up the api key
@pytest.fixture(autouse=True)
def setup_api_key():
    default_key = easypost.api_key
    easypost.api_key = EASYPOST_TEST_API_KEY
    yield
    easypost.api_key = default_key


# if a test needs to use the prod api key, make it depend on this fixture
@pytest.fixture
def prod_api_key():
    default_key = easypost.api_key
    easypost.api_key = EASYPOST_PROD_API_KEY
    yield
    easypost.api_key = default_key


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [
            ("authorization", "EZTK-NONE"),
            ("x-client-user-agent", "suppressed"),
            ("user-agent", "easypost/v2 pythonclient/suppressed"),
        ],
        "decode_compressed_response": True,
        "before_record_response": filter_response(),
        "record_mode": "once"
    }


def filter_response():
    def before_record_response(response):
            response['body']['string'] = response['body']['string'].decode('utf8')
            response_map = json.loads(response['body']['string'])

            if "id" in response_map.keys():
                response_map["id"] = "***"

            response_string = json.dumps(response_map)
            response['body']['string'] = response_string
            # breakpoint()
            return response
    return before_record_response


# We keep the page_size of retrieving `all` records small so cassettes stay small
@pytest.fixture
def page_size():
    return 5


# This is the USPS carrier account ID that comes with your EasyPost account by default and should be used for all tests
@pytest.fixture
def usps_carrier_account_id():
    # Fallback to the EasyPost Python Client Library Test User USPS carrier account ID
    return os.getenv("USPS_CARRIER_ACCOUNT_ID", "ca_b25657e9896e4d63ac8151ac346ac41e")


@pytest.fixture
def usps():
    return "USPS"


@pytest.fixture
def usps_service():
    return "First"


@pytest.fixture
def pickup_service():
    return "NextDay"


@pytest.fixture
def report_type():
    return "shipment"


# If you need to re-record cassettes, increment this date by 1
@pytest.fixture
def report_date():
    return "2022-04-11"


@pytest.fixture
def webhook_url():
    return "http://example.com"


@pytest.fixture
def basic_address():
    return {
        "name": "Jack Sparrow",
        "company": "EasyPost",
        "street1": "388 Townsend St",
        "street2": "Apt 20",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94107",
        "phone": "5555555555",
    }


@pytest.fixture
def incorrect_address_to_verify():
    return {
        "street1": "417 montgomery street",
        "street2": "FL 5",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94104",
        "country": "US",
        "company": "EasyPost",
        "phone": "415-123-4567",
    }


@pytest.fixture
def pickup_address():
    return {
        "name": "Dr. Steve Brule",
        "street1": "179 N Harbor Dr",
        "city": "Redondo Beach",
        "state": "CA",
        "zip": "90277",
        "country": "US",
        "phone": "3331114444",
    }


@pytest.fixture
def basic_parcel():
    return {
        "length": "10",
        "width": "8",
        "height": "4",
        "weight": "15.4",
    }


@pytest.fixture
def basic_customs_item():
    return {
        "description": "Sweet shirts",
        "quantity": 2,
        "weight": 11,
        "value": 23,
        "hs_tariff_number": "654321",
        "origin_country": "US",
    }


@pytest.fixture
def basic_customs_info(basic_customs_item):
    return {
        "eel_pfc": "NOEEI 30.37(a)",
        "customs_certify": True,
        "customs_signer": "Steve Brule",
        "contents_type": "merchandise",
        "contents_explanation": "",
        "restriction_type": "none",
        "non_delivery_option": "return",
        "customs_items": [
            basic_customs_item,
        ],
    }


@pytest.fixture
def tax_identifier():
    return {
        "entity": "SENDER",
        "tax_id_type": "IOSS",
        "tax_id": "12345",
        "issuing_country": "GB",
    }


@pytest.fixture
def basic_shipment(basic_address, basic_parcel):
    return {
        "to_address": basic_address,
        "from_address": basic_address,
        "parcel": basic_parcel,
    }


@pytest.fixture
def full_shipment(basic_address, basic_parcel, basic_customs_info):
    return {
        "to_address": basic_address,
        "from_address": basic_address,
        "parcel": basic_parcel,
        "customs_info": basic_customs_info,
        "options": {
            "label_format": "PNG",  # Must be PNG so we can convert to ZPL later
            "invoice_number": "123",
        },
        "reference": "123",
    }


@pytest.fixture
def one_call_buy_shipment(basic_address, basic_parcel, usps_service, usps_carrier_account_id, usps):
    return {
        "to_address": basic_address,
        "from_address": basic_address,
        "parcel": basic_parcel,
        "service": usps_service,
        "carrier_accounts": [usps_carrier_account_id],
        "carrier": usps,
    }


# This fixture will require you to add a `shipment` key with a Shipment object from a test.
# If you need to re-record cassettes, increment the date below and ensure it is one day in the future,
# USPS only does "next-day" pickups including Saturday but not Sunday or Holidays.
@pytest.fixture
def basic_pickup(basic_address):
    pickup_date = "2022-04-13"

    return {
        "address": basic_address,
        "min_datetime": pickup_date,
        "max_datetime": pickup_date,
        "instructions": "Pickup at front door",
    }


@pytest.fixture
def basic_carrier_account():
    return {
        "type": "UpsAccount",
        "credentials": {
            "account_number": "A1A1A1",
            "user_id": "USERID",
            "password": "PASSWORD",
            "access_license_number": "ALN",
        },
    }


# This fixture will require you to append a `tracking_code` key with the shipment's tracking code
@pytest.fixture
def basic_insurance(basic_address, usps):
    return {
        "to_address": basic_address,
        "from_address": basic_address,
        "carrier": usps,
        "amount": "100",
    }


@pytest.fixture
def basic_order(basic_address, basic_shipment):
    return {
        "to_address": basic_address,
        "from_address": basic_address,
        "shipments": [basic_shipment],
    }


@pytest.fixture
def event():
    return json.dumps(
        {
            "mode": "production",
            "description": "batch.created",
            "previous_attributes": {"state": "purchasing"},
            "pending_urls": ["example.com/easypost-webhook"],
            "completed_urls": [],
            "created_at": "2015-12-03T19:09:19Z",
            "updated_at": "2015-12-03T19:09:19Z",
            "result": {
                "id": "batch_...",
                "object": "Batch",
                "mode": "production",
                "state": "purchased",
                "num_shipments": 1,
                "reference": None,
                "created_at": "2015-12-03T19:09:19Z",
                "updated_at": "2015-12-03T19:09:19Z",
                "scan_form": None,
                "shipments": [{"batch_status": "postage_purchased", "batch_message": None, "id": "shp_123..."}],
                "status": {
                    "created": 0,
                    "queued_for_purchase": 0,
                    "creation_failed": 0,
                    "postage_purchased": 1,
                    "postage_purchase_failed": 0,
                },
                "pickup": None,
                "label_url": None,
            },
            "id": "evt_...",
            "object": "Event",
        }
    )
