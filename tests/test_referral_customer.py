import os
from unittest.mock import patch

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
def test_referral_customer_create(partner_user_prod_client):
    """This test requires a partner customer's production API key via PARTNER_USER_PROD_API_KEY."""
    created_referral_customer = partner_user_prod_client.referral_customer.create(
        name="test test",
        email="test@test.com",
        phone="8888888888",
    )

    assert isinstance(created_referral_customer, User)
    assert str.startswith(created_referral_customer.id, "user_")
    assert created_referral_customer.name == "test test"


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


@pytest.mark.skip("flow is deprecated, cannot easily be tested due to Stripe changes")
# PyVCR is having troubles matching the body of the form-encoded data here, override the default
@pytest.mark.vcr(
    match_on=[
        "headers",
        "method",
        "query",
        "uri",
    ]
)
def test_referral_customer_add_credit_card(partner_user_prod_client, credit_card_details):
    """This test requires a partner customer's production API key via PARTNER_USER_PROD_API_KEY
    as well as one of that customer's referral's production API keys via REFERRAL_CUSTOMER_PROD_API_KEY.
    """
    added_credit_card = partner_user_prod_client.referral_customer.add_credit_card(
        referral_api_key=REFERRAL_CUSTOMER_PROD_API_KEY,
        number=credit_card_details["number"],
        expiration_month=credit_card_details["expiration_month"],
        expiration_year=credit_card_details["expiration_year"],
        cvc=credit_card_details["cvc"],
    )

    assert str.startswith(added_credit_card.id, "pm_")
    assert added_credit_card.last4 == "6170"


@patch("easypost.services.referral_customer_service.ReferralCustomerService._retrieve_easypost_stripe_api_key")
@patch(
    "easypost.services.referral_customer_service.ReferralCustomerService._create_stripe_token",
    side_effect=Exception(),
)
def test_referral_add_credit_card_error(
    mock_stripe_token,
    mock_easypost_key,
    credit_card_details,
    partner_user_prod_client,
):
    """This test requires a partner customer's production API key via PARTNER_USER_PROD_API_KEY
    as well as one of that customer's referral's production API keys via REFERRAL_CUSTOMER_PROD_API_KEY.
    """
    with pytest.raises(Exception) as error:
        _ = partner_user_prod_client.referral_customer.add_credit_card(
            referral_api_key=REFERRAL_CUSTOMER_PROD_API_KEY,
            number=credit_card_details["number"],
            expiration_month=credit_card_details["expiration_month"],
            expiration_year=credit_card_details["expiration_year"],
            cvc=credit_card_details["cvc"],
        )

    assert str(error.value) == "Could not send card details to Stripe, please try again later."


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
