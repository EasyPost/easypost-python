import pytest

import easypost


@pytest.mark.vcr()
@pytest.mark.skip("Skipping due to the lack of an available real payment method in tests")
def test_billing_fund_wallet(prod_api_key):
    success = easypost.Billing.fund_wallet(
        amount="2000",
        primary_or_secondary="primary",
    )

    assert success is True


@pytest.mark.vcr()
@pytest.mark.skip("Skipping due to the lack of an available real payment method in tests")
def test_billing_payment_method_delete(prod_api_key):
    success = easypost.Billing.delete_payment_method(primary_or_secondary="primary")

    assert success is True


@pytest.mark.vcr()
@pytest.mark.skip("Skipping due to the lack of an available real payment method in tests")
def test_billing_retrieve_payment_methods(prod_api_key):
    payment_methods = easypost.Billing.retrieve_payment_methods()

    assert payment_methods is not None
