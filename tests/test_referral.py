import os

import pytest

import easypost


REFERRAL_USER_PROD_API_KEY = os.getenv("REFERRAL_USER_PROD_API_KEY", "123")


@pytest.mark.vcr()
def test_referral_user_create(partner_prod_api_key):
    """This test requires a partner user's production API key via EASYPOST_PROD_API_KEY."""
    created_referral_user = easypost.beta.Referral.create(
        name="test test",
        email="test@test.com",
        phone="8888888888",
    )

    assert isinstance(created_referral_user, easypost.User)
    assert str.startswith(created_referral_user.id, "user_")
    assert created_referral_user.name == "test test"


@pytest.mark.vcr()
def test_referral_user_update(partner_prod_api_key):
    """This test requires a partner user's production API key via EASYPOST_PROD_API_KEY."""
    referral_users = easypost.beta.Referral.all()

    updated_referral_user = easypost.beta.Referral.update_email(
        "email@example.com",
        referral_users.referral_customers[0].id,
    )

    assert updated_referral_user is True


@pytest.mark.vcr()
def test_referral_user_all(partner_prod_api_key, page_size):
    """This test requires a partner user's production API key via EASYPOST_PROD_API_KEY."""
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
def test_referral_add_credit_card(partner_prod_api_key, credit_card_details):
    """This test requires a partner user's production API key via EASYPOST_PROD_API_KEY
    as well as one of that user's referral's production API keys via REFERRAL_USER_PROD_API_KEY.
    """
    added_credit_card = easypost.beta.Referral.add_credit_card(
        referral_api_key=REFERRAL_USER_PROD_API_KEY,
        number=credit_card_details["number"],
        expiration_month=credit_card_details["expiration_month"],
        expiration_year=credit_card_details["expiration_year"],
        cvc=credit_card_details["cvc"],
    )

    assert str.startswith(added_credit_card.id, "card_")
    assert added_credit_card.last4 == "6170"
