import os
from unittest.mock import patch

import pytest

import easypost


REFERRAL_CUSTOMER_PROD_API_KEY = os.getenv("REFERRAL_CUSTOMER_PROD_API_KEY", "123")


@pytest.mark.vcr()
def test_beta_referral_user_create(partner_prod_api_key):
    """This test requires a partner user's production API key via PARTNER_USER_PROD_API_KEY."""
    created_referral_user = easypost.beta.Referral.create(
        name="test test",
        email="test@test.com",
        phone="8888888888",
    )

    assert isinstance(created_referral_user, easypost.User)
    assert str.startswith(created_referral_user.id, "user_")
    assert created_referral_user.name == "test test"


@pytest.mark.vcr()
def test_beta_referral_user_update(partner_prod_api_key):
    """This test requires a partner user's production API key via PARTNER_USER_PROD_API_KEY."""
    referral_users = easypost.beta.Referral.all()

    updated_referral_user = easypost.beta.Referral.update_email(
        "email@example.com",
        referral_users.referral_customers[0].id,
    )

    assert updated_referral_user is True


@pytest.mark.vcr()
def test_beta_referral_user_all(partner_prod_api_key, page_size):
    """This test requires a partner user's production API key via PARTNER_USER_PROD_API_KEY."""
    referral_users = easypost.beta.Referral.all(page_size=page_size)

    referral_users_array = referral_users["referral_customers"]

    assert len(referral_users_array) <= page_size
    assert referral_users["has_more"] is not None
    assert all(isinstance(referral_user, easypost.User) for referral_user in referral_users_array)


# PyVCR is having troubles matching the body of the form-encoded data here, override the default
@pytest.mark.vcr(
    match_on=[
        "headers",
        "method",
        "query",
        "uri",
    ]
)
def test_beta_referral_add_credit_card(partner_prod_api_key, credit_card_details):
    """This test requires a partner user's production API key via PARTNER_USER_PROD_API_KEY
    as well as one of that user's referral's production API keys via REFERRAL_CUSTOMER_PROD_API_KEY.
    """
    added_credit_card = easypost.beta.Referral.add_credit_card(
        referral_api_key=REFERRAL_CUSTOMER_PROD_API_KEY,
        number=credit_card_details["number"],
        expiration_month=credit_card_details["expiration_month"],
        expiration_year=credit_card_details["expiration_year"],
        cvc=credit_card_details["cvc"],
    )

    assert str.startswith(added_credit_card.id, "card_")
    assert added_credit_card.last4 == "6170"


@patch("easypost.beta.referral.Referral._retrieve_easypost_stripe_api_key")
@patch("easypost.beta.referral.Referral._create_stripe_token", side_effect=Exception())
def test_beta_referral_add_credit_card_error(mock_stripe_token, mock_easypost_key, credit_card_details):
    """This test requires a partner user's production API key via PARTNER_USER_PROD_API_KEY
    as well as one of that user's referral's production API keys via REFERRAL_CUSTOMER_PROD_API_KEY.
    """
    with pytest.raises(Exception) as error:
        _ = easypost.beta.Referral.add_credit_card(
            referral_api_key=REFERRAL_CUSTOMER_PROD_API_KEY,
            number=credit_card_details["number"],
            expiration_month=credit_card_details["expiration_month"],
            expiration_year=credit_card_details["expiration_year"],
            cvc=credit_card_details["cvc"],
        )

    assert str(error.value) == "Could not send card details to Stripe, please try again later"


@pytest.mark.vcr()
def test_beta_referral_add_payment_method(referral_customer_prod_api_key):
    """This test requires a referral customer user's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid Stripe details to use. Assert the correct error.
    """
    with pytest.raises(Exception) as error:
        easypost.beta.Referral.add_payment_method(
            stripe_customer_id="cus_123",
            payment_method_reference="ba_123",
            primary_or_secondary="primary",
        )

    assert str(error.value) == "Invalid Payment Gateway Reference."


@pytest.mark.vcr()
def test_beta_referral_refund_by_amount(referral_customer_prod_api_key):
    """This test requires a referral customer user's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid billing details to use. Assert the correct error.
    """
    with pytest.raises(Exception) as error:
        easypost.beta.Referral.refund_by_amount(refund_amount=2000)

    assert str(error.value) == "Refund amount is invalid. Please use a valid amount or escalate to finance."


@pytest.mark.vcr()
def test_beta_referral_refund_by_payment_log(referral_customer_prod_api_key):
    """This test requires a referral customer user's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid billing details to use. Assert the correct error.
    """
    with pytest.raises(Exception) as error:
        easypost.beta.Referral.refund_by_payment_log(payment_log_id="paylog_123")

    assert str(error.value) == "We could not find a transaction with that id."
