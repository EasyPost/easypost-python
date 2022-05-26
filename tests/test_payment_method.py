import pytest

import easypost


@pytest.mark.vcr()
def test_payment_method_all(prod_api_key):
    payment_methods = easypost.PaymentMethod.all()

    assert hasattr(payment_methods, "primary_payment_method")
    assert hasattr(payment_methods, "secondary_payment_method")
