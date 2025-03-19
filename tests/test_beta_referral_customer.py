import pytest
from easypost.errors.api.api_error import ApiError


@pytest.mark.vcr()
def test_beta_referral_customer_add_payment_method(referral_customer_prod_client, billing):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid Stripe details to use. Assert the correct error.
    """
    with pytest.raises(ApiError) as error:
        referral_customer_prod_client.beta_referral_customer.add_payment_method(
            stripe_customer_id="cus_123",
            payment_method_reference="ba_123",
            priority=billing["priority"],
        )

    assert str(error.value) == "Invalid connect integration."


@pytest.mark.vcr()
def test_beta_referral_customer_refund_by_amount(referral_customer_prod_client):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid billing details to use. Assert the correct error.
    """
    with pytest.raises(ApiError) as error:
        referral_customer_prod_client.beta_referral_customer.refund_by_amount(refund_amount=2000)

    assert str(error.value) == "Refund amount is invalid. Please use a valid amount or escalate to finance."


@pytest.mark.vcr()
def test_beta_referral_customer_refund_by_payment_log(referral_customer_prod_client):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid billing details to use. Assert the correct error.
    """
    with pytest.raises(ApiError) as error:
        referral_customer_prod_client.beta_referral_customer.refund_by_payment_log(payment_log_id="paylog_123")

    assert str(error.value) == "We could not find a transaction with that id."


@pytest.mark.vcr()
def test_beta_referral_customer_create_credit_card_client_secret(referral_customer_prod_client):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY."""
    response = referral_customer_prod_client.beta_referral_customer.create_credit_card_client_secret()

    assert str.startswith(response.client_secret, "seti_")


@pytest.mark.vcr()
def test_beta_referral_customer_create_bank_account_client_secret(referral_customer_prod_client):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY."""
    response = referral_customer_prod_client.beta_referral_customer.create_bank_account_client_secret()

    assert str.startswith(response.client_secret, "fcsess_client_secret_")
