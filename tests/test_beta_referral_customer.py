import pytest

import easypost


@pytest.mark.vcr()
def test_beta_referral_customer_add_payment_method(referral_customer_prod_api_key):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid Stripe details to use. Assert the correct error.
    """
    with pytest.raises(Exception) as error:
        easypost.beta.ReferralCustomer.add_payment_method(
            stripe_customer_id="cus_123",
            payment_method_reference="ba_123",
            primary_or_secondary="primary",
        )

    assert str(error.value) == "Invalid Payment Gateway Reference."


@pytest.mark.vcr()
def test_beta_referral_customer_refund_by_amount(referral_customer_prod_api_key):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid billing details to use. Assert the correct error.
    """
    with pytest.raises(Exception) as error:
        easypost.beta.ReferralCustomer.refund_by_amount(refund_amount=2000)

    assert str(error.value) == "Refund amount is invalid. Please use a valid amount or escalate to finance."


@pytest.mark.vcr()
def test_beta_referral_customer_refund_by_payment_log(referral_customer_prod_api_key):
    """This test requires a referral customer's production API key via REFERRAL_CUSTOMER_PROD_API_KEY.

    We expect this test to fail because we don't have valid billing details to use. Assert the correct error.
    """
    with pytest.raises(Exception) as error:
        easypost.beta.ReferralCustomer.refund_by_payment_log(payment_log_id="paylog_123")

    assert str(error.value) == "We could not find a transaction with that id."
