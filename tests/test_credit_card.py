import pytest

import easypost


@pytest.mark.vcr()
@pytest.mark.skip("Skipping due to the lack of an available real credit card in tests")
def test_credit_card_fund(prod_api_key):
    credit_card = easypost.CreditCard.fund("100", "primary")

    assert credit_card


@pytest.mark.vcr()
@pytest.mark.skip("Skipping due to the lack of an available real credit card in tests")
def test_credit_card_delete(prod_api_key):
    credit_card = easypost.CreditCard.delete("card_123")

    assert credit_card
