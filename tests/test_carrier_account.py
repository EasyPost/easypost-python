import pytest
from easypost.errors.api.api_error import ApiError
from easypost.models import CarrierAccount


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
def test_carrier_account_create_with_custom_workflow(prod_client):
    """Test register a Carrier Account with custom registration such as FedEx or UPS.

    We purposefully don't pass data here because real data is required for this endpoint
    which we don't have in a test context, simply assert the error matches when no data is passed.
    """
    carrier_account = {
        "type": "UpsAccount",
        "registration_data": {},
    }

    try:
        prod_client.carrier_account.create(**carrier_account)
    except ApiError as error:
        assert error.http_status == 422
        assert any(
            [error["field"] == "account_number" and error["message"] == "must be present and a string"]
            for error in error.errors
        )
