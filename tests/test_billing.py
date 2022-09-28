from unittest.mock import patch

import pytest

import easypost


@patch("easypost.billing.Billing._get_payment_method_info", return_value=["endpoint", "card_123"])
@patch("easypost.billing.Requestor.request", return_value=[{"mock": "response"}, "mock-api-key"])
def test_billing_fund_wallet(mock_request, mock_get_payment_info):
    success = easypost.Billing.fund_wallet(
        amount="2000",
        primary_or_secondary="primary",
    )

    assert success is True


@patch("easypost.billing.Billing.retrieve_payment_methods", return_value={"primary_payment_method": {"id": "card_123"}})
@patch("easypost.billing.Requestor.request", return_value=[{"mock": "response"}, "mock-api-key"])
def test_billing_payment_method_delete_credit_card(mock_request, mock_payment_methods):
    """Tests we make a valid call to delete a credit card."""
    success = easypost.Billing.delete_payment_method(primary_or_secondary="primary")

    mock_request.assert_called_once_with(method=easypost.requestor.RequestMethod.DELETE, url="/credit_cards/card_123")
    assert success is True


@patch("easypost.billing.Billing.retrieve_payment_methods", return_value={"primary_payment_method": {"id": "bank_123"}})
@patch("easypost.billing.Requestor.request", return_value=[{"mock": "response"}, "mock-api-key"])
def test_billing_payment_method_delete_bank_account(mock_request, mock_payment_methods):
    """Tests we make a valid call to delete a bank account."""
    success = easypost.Billing.delete_payment_method(primary_or_secondary="primary")

    mock_request.assert_called_once_with(method=easypost.requestor.RequestMethod.DELETE, url="/bank_accounts/bank_123")
    assert success is True


@patch("easypost.billing.Billing.retrieve_payment_methods", return_value={"primary_payment_method": {"id": "bad_id"}})
@patch("easypost.billing.Requestor.request", return_value=[{"mock": "response"}, "mock-api-key"])
def test_billing_payment_method_delete_invalid(mock_request, mock_payment_methods):
    """Tests we raise an error when we receive an invalid payment method"""
    with pytest.raises(easypost.Error):
        _ = easypost.Billing.delete_payment_method(primary_or_secondary="primary")


@patch("easypost.billing.Billing.retrieve_payment_methods", return_value={"primary_payment_methods": {"id": "bad_id"}})
@patch("easypost.billing.Requestor.request", return_value=[{"mock": "response"}, "mock-api-key"])
def test_billing_payment_method_delete_bad_request(mock_request, mock_payment_methods):
    """Tests we raise an error when we cannot retrieve a payment method."""
    with pytest.raises(easypost.Error):
        _ = easypost.Billing.delete_payment_method(primary_or_secondary="tertiary")


@patch("easypost.billing.Requestor.request", return_value=[{"id": "card_123"}, "mock-api-key"])
def test_billing_retrieve_payment_methods(mock_request):
    """Tests that we throw an error when we cannot retrieve payment methods due to no billing being setup."""
    response = easypost.Billing.retrieve_payment_methods()

    mock_request.assert_called_once_with(method=easypost.requestor.RequestMethod.GET, url="/payment_methods", params={})
    assert isinstance(response, easypost.easypost_object.EasyPostObject)


@patch("easypost.billing.Requestor.request", return_value=[{"mock": "response"}, "mock-api-key"])
def test_billing_retrieve_payment_methods_no_billing_setup(mock_request):
    """Tests that we throw an error when we cannot retrieve payment methods due to no billing being setup."""
    with pytest.raises(easypost.Error) as error:
        _ = easypost.Billing.retrieve_payment_methods()

    mock_request.assert_called_once()
    assert str(error.value) == "Billing has not been setup for this user. Please add a payment method."
