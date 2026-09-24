import os

import pytest

from easypost.constant import (
    _FILTERS_KEY,
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.errors.api.api_error import ApiError
from easypost.models import User

REFERRAL_CUSTOMER_PROD_API_KEY = os.getenv("REFERRAL_CUSTOMER_PROD_API_KEY", "123")


@pytest.mark.vcr()
def test_referral_customer_create(partner_user_prod_client, referral_user):
    """This test requires a partner customer's production API key via PARTNER_USER_PROD_API_KEY."""
    created_referral_customer = partner_user_prod_client.referral_customer.create(
        name=referral_user["name"],
        email=referral_user["email"],
        phone=referral_user["phone"],
    )

    assert isinstance(created_referral_customer, User)
    assert str.startswith(created_referral_customer.id, "user_")
    assert created_referral_customer.name == "Test Referral"


@pytest.mark.vcr()
def test_referral_customer_update(partner_user_prod_client):
    """This test requires a partner customer's production API key via PARTNER_USER_PROD_API_KEY."""
    referral_customers = partner_user_prod_client.referral_customer.all()

    try:
        partner_user_prod_client.referral_customer.update_email(
            referral_customers.referral_customers[0].id,
            "email@example.com",
        )
    except Exception:
        assert False


@pytest.mark.vcr()
def test_referral_customer_all(partner_user_prod_client, page_size):
    """This test requires a partner customer's production API key via PARTNER_USER_PROD_API_KEY."""
    referral_customers = partner_user_prod_client.referral_customer.all(page_size=page_size)

    referral_customers_array = referral_customers["referral_customers"]

    assert len(referral_customers_array) <= page_size
    assert referral_customers["has_more"] is not None
    assert all(isinstance(referral_customer, User) for referral_customer in referral_customers_array)


@pytest.mark.vcr()
def test_referral_get_next_page(partner_user_prod_client, page_size):
    try:
        first_page = partner_user_prod_client.referral_customer.all(page_size=page_size)
        next_page = partner_user_prod_client.referral_customer.get_next_page(
            referral_customers=first_page, page_size=page_size
        )

        first_id_of_first_page = first_page["referral_customers"][0].id
        first_id_of_second_page = next_page["referral_customers"][0].id

        assert first_id_of_first_page != first_id_of_second_page

        # Verify that the filters are being passed along for behind-the-scenes reference
        assert first_page[_FILTERS_KEY] == next_page[_FILTERS_KEY]
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(_TEST_FAILED_INTENTIONALLY_ERROR)


@pytest.mark.vcr()
def test_referral_customer_add_credit_card_from_stripe(partner_user_prod_client, credit_card_details, billing):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid billing details to use. Assert the correct error.
    """
    with pytest.raises(ApiError) as error:
        partner_user_prod_client.referral_customer.add_credit_card_from_stripe(
            referral_api_key=REFERRAL_CUSTOMER_PROD_API_KEY,
            payment_method_id=billing["payment_method_id"],
            priority=billing["priority"],
        )

    assert str(error.value) == "Stripe::PaymentMethod does not exist for the specified reference_id"


@pytest.mark.vcr()
def test_referral_customer_add_bank_account_from_stripe(partner_user_prod_client, credit_card_details, billing):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid billing details to use. Assert the correct error.
    """
    with pytest.raises(ApiError) as error:
        partner_user_prod_client.referral_customer.add_bank_account_from_stripe(
            referral_api_key=REFERRAL_CUSTOMER_PROD_API_KEY,
            financial_connections_id=billing["financial_connections_id"],
            mandate_data=billing["mandate_data"],
            priority=billing["priority"],
        )

    assert (
        str(error.value) == "account_holder_name must be present when creating a Financial Connections payment method"
    )


@pytest.mark.vcr()
def test_referral_customer_retrieve_easypost_stripe_api_key(partner_user_prod_client):
    """This test requires a partner customer's production API key via PARTNER_USER_PROD_API_KEY."""
    public_key = partner_user_prod_client.referral_customer.retrieve_easypost_stripe_api_key()

    assert isinstance(public_key, str)
    assert public_key.startswith("pk_")
