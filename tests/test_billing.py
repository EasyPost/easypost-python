from unittest.mock import patch

import easypost
import pytest
from easypost.errors import InvalidObjectError


@patch(
    "easypost.services.billing_service.BillingService._get_payment_method_info", return_value=["/endpoint", "card_123"]
)
@patch("easypost.services.billing_service.Requestor.request", return_value={"mock": "response"})
def test_billing_fund_wallet(mock_request, mock_get_payment_info, prod_client):
    prod_client.billing.fund_wallet(
        amount="2000",
        priority="primary",
    )

    mock_request.assert_called_once_with(
        method=easypost.requestor.RequestMethod.POST,
        url="/endpoint/card_123/charges",
        params={"amount": "2000"},
    )


@patch(
    "easypost.services.billing_service.BillingService.retrieve_payment_methods",
    return_value={"primary_payment_method": {"id": "card_123"}},
)
@patch("easypost.services.billing_service.Requestor.request", return_value={"mock": "response"})
def test_billing_payment_method_delete_credit_card(mock_request, mock_payment_methods, prod_client):
    """Tests we make a valid call to delete a credit card."""
    prod_client.billing.delete_payment_method(priority="primary")

    mock_request.assert_called_once_with(method=easypost.requestor.RequestMethod.DELETE, url="/credit_cards/card_123")


@patch(
    "easypost.services.billing_service.BillingService.retrieve_payment_methods",
    return_value={"primary_payment_method": {"id": "bank_123"}},
)
@patch("easypost.services.billing_service.Requestor.request", return_value={"mock": "response"})
def test_billing_payment_method_delete_bank_account(mock_request, mock_payment_methods, prod_client):
    """Tests we make a valid call to delete a bank account."""
    prod_client.billing.delete_payment_method(priority="primary")

    mock_request.assert_called_once_with(method=easypost.requestor.RequestMethod.DELETE, url="/bank_accounts/bank_123")


@patch(
    "easypost.services.billing_service.BillingService.retrieve_payment_methods",
    return_value={"primary_payment_method": {"id": "bad_id"}},
)
@patch("easypost.services.billing_service.Requestor.request", return_value={"mock": "response"})
def test_billing_payment_method_delete_invalid(mock_request, mock_payment_methods, prod_client):
    """Tests we raise an error when we receive an invalid payment method"""
    with pytest.raises(InvalidObjectError):
        _ = prod_client.billing.delete_payment_method(priority="primary")


@patch(
    "easypost.services.billing_service.BillingService.retrieve_payment_methods",
    return_value={"primary_payment_methods": {"id": "bad_id"}},
)
@patch("easypost.services.billing_service.Requestor.request", return_value={"mock": "response"})
def test_billing_payment_method_delete_bad_request(mock_request, mock_payment_methods, prod_client):
    """Tests we raise an error when we cannot retrieve a payment method."""
    with pytest.raises(InvalidObjectError):
        _ = prod_client.billing.delete_payment_method(priority="tertiary")


@patch("easypost.services.billing_service.Requestor.request", return_value={"id": "card_123"})
def test_billing_retrieve_payment_methods(mock_request, prod_client):
    """Tests that we throw an error when we cannot retrieve payment methods due to no billing being setup."""
    response = prod_client.billing.retrieve_payment_methods()

    mock_request.assert_called_once_with(method=easypost.requestor.RequestMethod.GET, url="/payment_methods", params={})
    assert isinstance(response, easypost.easypost_object.EasyPostObject)


@patch("easypost.services.billing_service.Requestor.request", return_value={"mock": "response"})
def test_billing_retrieve_payment_methods_no_billing_setup(mock_request, prod_client):
    """Tests that we throw an error when we cannot retrieve payment methods due to no billing being setup."""
    with pytest.raises(InvalidObjectError) as error:
        _ = prod_client.billing.retrieve_payment_methods()

    mock_request.assert_called_once()
    assert str(error.value) == "Billing has not been setup for this user. Please add a payment method."
