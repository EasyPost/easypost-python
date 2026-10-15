import pytest

from easypost.constant import _CARRIER_ACCOUNT_CREATE_ENDPOINT_TYPES
from easypost.errors.api.api_error import ApiError
from easypost.models import CarrierAccount
from easypost.requestor import Requestor


@pytest.fixture
def vcr_cassette_name(request):
    return request.node.name.replace("[", "_").replace("]", "")


def _flatten_custom_carrier_route_mapping():
    return [
        (carrier_account_type, endpoint)
        for endpoint, carrier_account_types in _CARRIER_ACCOUNT_CREATE_ENDPOINT_TYPES.items()
        for carrier_account_type in carrier_account_types
    ]


def _carrier_create_payload_for_endpoint(endpoint: str) -> dict:
    if endpoint in ("/carrier_accounts/open", "/carrier_accounts/register"):
        return {"registration_data": {}}

    return {}


@pytest.mark.vcr()
def test_carrier_account_create(prod_client, basic_carrier_account):
    carrier_account = prod_client.carrier_account.create(**basic_carrier_account)

    assert isinstance(carrier_account, CarrierAccount)
    assert str.startswith(carrier_account.id, "ca_")
    assert carrier_account.type == "DhlEcsAccount"

    prod_client.carrier_account.delete(carrier_account.id)  # Delete the carrier account once it's done being tested.


@pytest.mark.vcr()
def test_carrier_account_retrieve(prod_client, basic_carrier_account):
    carrier_account = prod_client.carrier_account.create(**basic_carrier_account)

    retrieved_carrier_account = prod_client.carrier_account.retrieve(carrier_account.id)

    assert isinstance(retrieved_carrier_account, CarrierAccount)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert carrier_account.id == retrieved_carrier_account.id

    prod_client.carrier_account.delete(
        retrieved_carrier_account.id
    )  # Delete the carrier account once it's done being tested.


@pytest.mark.vcr()
def test_carrier_account_all(prod_client, page_size):
    carrier_accounts = prod_client.carrier_account.all(page_size=page_size)

    assert all(isinstance(carrier_account, CarrierAccount) for carrier_account in carrier_accounts)


@pytest.mark.vcr()
def test_carrier_account_update(prod_client, basic_carrier_account):
    carrier_account = prod_client.carrier_account.create(**basic_carrier_account)

    test_description = "My custom description"

    updated_carrier_account = prod_client.carrier_account.update(
        carrier_account.id,
        description=test_description,
    )

    assert isinstance(updated_carrier_account, CarrierAccount)
    assert str.startswith(updated_carrier_account.id, "ca_")
    assert updated_carrier_account.description == test_description

    prod_client.carrier_account.delete(
        updated_carrier_account.id
    )  # Delete the carrier account once it's done being tested.


@pytest.mark.vcr()
def test_carrier_account_delete(prod_client, basic_carrier_account):
    carrier_account = prod_client.carrier_account.create(**basic_carrier_account)

    try:
        prod_client.carrier_account.delete(carrier_account.id)
    except Exception:
        assert False


@pytest.mark.vcr()
def test_carrier_account_type(prod_client):
    types = prod_client.carrier_account.types()

    assert isinstance(types, list)


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "carrier_account_type,expected_endpoint,params",
    [
        pytest.param(
            carrier_account_type,
            endpoint,
            _carrier_create_payload_for_endpoint(endpoint),
            id=carrier_account_type,
        )
        for carrier_account_type, endpoint in _flatten_custom_carrier_route_mapping()
    ],
)
def test_carrier_account_create_url_routing(prod_client, monkeypatch, carrier_account_type, expected_endpoint, params):
    payload = {"type": carrier_account_type, **params}
    captured_request = {}

    original_request = Requestor.request

    def spy_request(self, method, url, params=None, *args, **kwargs):
        if "url" not in captured_request and url.startswith("/carrier_accounts"):
            captured_request["url"] = url
            captured_request["params"] = params
        return original_request(self, method, url, params, *args, **kwargs)

    monkeypatch.setattr(Requestor, "request", spy_request)

    try:
        carrier_account = prod_client.carrier_account.create(**payload)
    except ApiError as error:
        assert error.http_status not in (404, 500)
    else:
        assert isinstance(carrier_account, CarrierAccount)
        assert str.startswith(carrier_account.id, "ca_")
        prod_client.carrier_account.delete(carrier_account.id)

    assert captured_request["url"] == expected_endpoint
    if expected_endpoint == "/carrier_accounts/register_oauth":
        assert "carrier_account_oauth_registrations" in captured_request["params"]
    else:
        assert "carrier_account" in captured_request["params"]
