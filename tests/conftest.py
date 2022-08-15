import json
import os
from typing import List

import pytest

import easypost


EASYPOST_TEST_API_KEY = os.environ["EASYPOST_TEST_API_KEY"]
EASYPOST_PROD_API_KEY = os.environ["EASYPOST_PROD_API_KEY"]
PARTNER_USER_PROD_API_KEY = os.environ["PARTNER_USER_PROD_API_KEY", "123"]

CASSETTE_REPLACEMENT_VALUE = "<REDACTED>"


def pytest_sessionstart(session):
    """This is for local unit testing with google appengine, otherwise you get a
    'No api proxy found for service "urlfetch"' response.
    """
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


@pytest.fixture(autouse=True)
def setup_api_key():
    """This fixture is auto-loaded by all tests; it sets up the api key."""
    default_key = easypost.api_key
    easypost.api_key = EASYPOST_TEST_API_KEY
    yield
    easypost.api_key = default_key


@pytest.fixture
def prod_api_key():
    """If a test needs to use the prod api key, make it depend on this fixture."""
    default_key = easypost.api_key
    easypost.api_key = EASYPOST_PROD_API_KEY
    yield
    easypost.api_key = default_key


@pytest.fixture
def partner_prod_api_key():
    """If a test needs to use the partner prod api key, make it depend on this fixture."""
    default_key = easypost.api_key
    easypost.api_key = PARTNER_USER_PROD_API_KEY
    yield
    easypost.api_key = default_key


@pytest.fixture(scope="session")
def vcr_config():
    """Setup the VCR config for the test suite."""
    return {
        "match_on": [
            "body",
            "headers",
            "method",
            "query",
            "uri",
        ],
        "decode_compressed_response": True,
        "filter_headers": [
            ("authorization", CASSETTE_REPLACEMENT_VALUE),
            ("user-agent", CASSETTE_REPLACEMENT_VALUE),
        ],
        "filter_query_parameters": [
            "card[number]",
            "card[cvc]",
        ],
        "before_record_response": scrub_response_bodies(
            scrubbers=[
                "api_keys",
                "children",
                "client_ip",
                "credentials",
                "email",
                "key",
                "keys",
                "phone_number",
                "phone",
                "test_credentials",
            ]
        ),
    }


def scrub_response_bodies(scrubbers: List[str]):
    """Scrub sensitive data from response bodies (at the root level or in a root list)
    prior to recording the cassette.

    This function DOES NOT scrub data in nested objects or lists.
    """

    def before_record_response(response):
        if response["body"]["string"]:
            response_body = json.loads(response["body"]["string"].decode())
            for scrubber in scrubbers:
                if isinstance(response_body, list):
                    for element in response_body:
                        if scrubber in element:
                            element[scrubber] = CASSETTE_REPLACEMENT_VALUE
                else:
                    if scrubber in response_body:
                        response_body[scrubber] = CASSETTE_REPLACEMENT_VALUE

            response["body"]["string"] = json.dumps(response_body).encode()
        return response

    return before_record_response


def read_fixture_data():
    """Reads fixture data from the fixtures JSON file."""
    with open(os.path.join("examples", "official", "fixtures", "client-library-fixtures.json")) as data:
        fixtures = json.load(data)

    return fixtures


@pytest.fixture
def page_size():
    """We keep the page_size of retrieving `all` records small so cassettes stay small."""
    return read_fixture_data()["page_sizes"]["five_results"]


@pytest.fixture
def usps_carrier_account_id():
    """This is the USPS carrier account ID that comes with your
    EasyPost account by default and should be used for all tests.
    """
    # Fallback to the EasyPost Python Client Library Test User USPS carrier account ID due to strict matching
    return os.getenv("USPS_CARRIER_ACCOUNT_ID", "ca_b25657e9896e4d63ac8151ac346ac41e")


@pytest.fixture
def usps():
    return read_fixture_data()["carrier_strings"]["usps"]


@pytest.fixture
def usps_service():
    return read_fixture_data()["service_names"]["usps"]["first_service"]


@pytest.fixture
def pickup_service():
    return read_fixture_data()["service_names"]["usps"]["pickup_service"]


@pytest.fixture
def report_type():
    return read_fixture_data()["report_types"]["shipment"]


@pytest.fixture
def report_date():
    return "2022-05-04"


@pytest.fixture
def webhook_url():
    return read_fixture_data()["webhook_url"]


@pytest.fixture
def ca_address_1():
    return read_fixture_data()["addresses"]["ca_address_1"]


@pytest.fixture
def ca_address_2():
    return read_fixture_data()["addresses"]["ca_address_2"]


@pytest.fixture
def incorrect_address():
    return read_fixture_data()["addresses"]["incorrect"]


@pytest.fixture
def basic_parcel():
    return read_fixture_data()["parcels"]["basic"]


@pytest.fixture
def basic_customs_item():
    return read_fixture_data()["customs_items"]["basic"]


@pytest.fixture
def basic_customs_info():
    return read_fixture_data()["customs_infos"]["basic"]


@pytest.fixture
def tax_identifier():
    return read_fixture_data()["tax_identifiers"]["basic"]


@pytest.fixture
def basic_shipment():
    return read_fixture_data()["shipments"]["basic_domestic"]


@pytest.fixture
def full_shipment():
    return read_fixture_data()["shipments"]["full"]


@pytest.fixture
def one_call_buy_shipment(ca_address_1, ca_address_2, basic_parcel, usps_service, usps_carrier_account_id, usps):
    return {
        "to_address": ca_address_1,
        "from_address": ca_address_2,
        "parcel": basic_parcel,
        "service": usps_service,
        "carrier_accounts": [usps_carrier_account_id],
        "carrier": usps,
    }


@pytest.fixture
def basic_pickup():
    """This fixture will require you to add a `shipment` key with a Shipment object from a test.
    If you need to re-record cassettes, increment the date below and ensure it is one day in the future,
    USPS only does "next-day" pickups including Saturday but not Sunday or Holidays.
    """
    pickup_date = "2022-08-17"

    pickup_data = read_fixture_data()["pickups"]["basic"]
    pickup_data["min_datetime"] = pickup_date
    pickup_data["max_datetime"] = pickup_date

    return pickup_data


@pytest.fixture
def basic_carrier_account():
    return read_fixture_data()["carrier_accounts"]["basic"]


@pytest.fixture
def basic_insurance():
    """This fixture will require you to append a `tracking_code` key with the shipment's tracking code."""
    return read_fixture_data()["insurances"]["basic"]


@pytest.fixture
def basic_order():
    return read_fixture_data()["orders"]["basic"]


@pytest.fixture
def event_json():
    return json.dumps(read_fixture_data()["event_body"])


@pytest.fixture
def event_bytes():
    data = read_fixture_data()["event_body"]

    return json.dumps(data, separators=(",", ":")).encode()


@pytest.fixture
def credit_card_details():
    """The credit card details below are for a valid proxy card usable
    for tests only and cannot be used for real transactions.

    DO NOT alter these details with real credit card information.
    """
    return read_fixture_data()["credit_cards"]["test"]


@pytest.fixture
def rma_form_options():
    return read_fixture_data()["form_options"]["rma"]
