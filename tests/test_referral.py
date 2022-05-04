import pytest

import easypost


@pytest.mark.vcr()
@pytest.mark.skip(reason="Do not record this test in cassette because there is sensitive info")
def test_referral_user_create(prod_api_key):
    created_referral_user = easypost.beta.Referral.create(
        name="test test",
        email="test@test.com",
        phone="8888888888",
    )

    assert isinstance(created_referral_user, easypost.User)
    assert str.startswith(created_referral_user.id, "user_")
    assert created_referral_user.phone_number == "8888888888"


@pytest.mark.vcr()
def test_referral_user_update(prod_api_key):
    referral_users = easypost.beta.Referral.all()

    updated_referral_user = easypost.beta.Referral.update_email(
        "email@example.com",
        referral_users[0].id,
    )

    assert updated_referral_user is True


@pytest.mark.vcr()
def test_referral_user_all(prod_api_key, page_size):
    referral_users = easypost.beta.Referral.all(page_size=page_size)

    assert len(referral_users) <= page_size
    assert all(isinstance(referral_user, easypost.User) for referral_user in referral_users)


@pytest.mark.vcr()
@pytest.mark.skip(reason="Do not record this test in cassette because there is sensitive info")
def test_referral_add_credit_card(prod_api_key):
    added_credit_card = easypost.beta.Referral.add_credit_card(
        "your_referral_api_key",
        "1234567890",
        "00",
        "0000",
        "000",
    )

    assert str.startswith(added_credit_card.id, "card_")
    assert str.startswith(added_credit_card.last4, "7890")
