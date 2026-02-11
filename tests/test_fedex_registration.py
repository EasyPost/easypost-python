from unittest.mock import MagicMock

from easypost.easypost_object import EasyPostObject
from easypost.models import CarrierAccount


def test_register_address(prod_client, monkeypatch):
    """Tests registering a billing address."""
    fedex_account_number = "123456789"
    address_validation = {
        "name": "BILLING NAME",
        "street1": "1234 BILLING STREET",
        "city": "BILLINGCITY",
        "state": "ST",
        "postal_code": "12345",
        "country_code": "US",
    }
    easypost_details = {"carrier_account_id": "ca_123"}
    params = {
        "address_validation": address_validation,
        "easypost_details": easypost_details,
    }

    json_response = {
        "email_address": None,
        "options": ["SMS", "CALL", "INVOICE"],
        "phone_number": "***-***-9721",
    }

    mock_requestor = MagicMock()
    mock_requestor.return_value.request.return_value = json_response

    monkeypatch.setattr("easypost.services.fedex_registration_service.Requestor", mock_requestor)

    response = prod_client.fedex_registration.register_address(fedex_account_number, **params)
    assert isinstance(response, EasyPostObject)
    assert response.email_address is None
    assert "SMS" in response.options
    assert "CALL" in response.options
    assert "INVOICE" in response.options
    assert response.phone_number == "***-***-9721"


def test_request_pin(prod_client, monkeypatch):
    """Tests requesting a pin."""
    fedex_account_number = "123456789"

    json_response = {"message": "sent secured Pin"}

    mock_requestor = MagicMock()
    mock_requestor.return_value.request.return_value = json_response

    monkeypatch.setattr("easypost.services.fedex_registration_service.Requestor", mock_requestor)

    response = prod_client.fedex_registration.request_pin(fedex_account_number, "SMS")
    assert isinstance(response, EasyPostObject)
    assert response.message == "sent secured Pin"


def test_validate_pin(prod_client, monkeypatch):
    """Tests validating a pin."""
    fedex_account_number = "123456789"
    pin_validation = {
        "pin_code": "123456",
        "name": "BILLING NAME",
    }
    easypost_details = {"carrier_account_id": "ca_123"}
    params = {
        "pin_validation": pin_validation,
        "easypost_details": easypost_details,
    }

    json_response = {
        "id": "ca_123",
        "object": "CarrierAccount",
        "type": "FedexAccount",
        "credentials": {
            "account_number": "123456789",
            "mfa_key": "123456789-XXXXX",
        },
    }

    mock_requestor = MagicMock()
    mock_requestor.return_value.request.return_value = json_response

    monkeypatch.setattr("easypost.services.fedex_registration_service.Requestor", mock_requestor)

    response = prod_client.fedex_registration.validate_pin(fedex_account_number, **params)
    assert isinstance(response, CarrierAccount)
    assert response.id == "ca_123"
    assert response.object == "CarrierAccount"
    assert response.type == "FedexAccount"
    assert response.credentials["account_number"] == "123456789"
    assert response.credentials["mfa_key"] == "123456789-XXXXX"


def test_submit_invoice(prod_client, monkeypatch):
    """Tests submitting details about an invoice."""
    fedex_account_number = "123456789"
    invoice_validation = {
        "name": "BILLING NAME",
        "invoice_number": "INV-12345",
        "invoice_date": "2025-12-08",
        "invoice_amount": "100.00",
        "invoice_currency": "USD",
    }
    easypost_details = {"carrier_account_id": "ca_123"}
    params = {
        "invoice_validation": invoice_validation,
        "easypost_details": easypost_details,
    }

    json_response = {
        "id": "ca_123",
        "object": "CarrierAccount",
        "type": "FedexAccount",
        "credentials": {
            "account_number": "123456789",
            "mfa_key": "123456789-XXXXX",
        },
    }

    mock_requestor = MagicMock()
    mock_requestor.return_value.request.return_value = json_response

    monkeypatch.setattr("easypost.services.fedex_registration_service.Requestor", mock_requestor)

    response = prod_client.fedex_registration.submit_invoice(fedex_account_number, **params)
    assert isinstance(response, CarrierAccount)
    assert response.id == "ca_123"
    assert response.object == "CarrierAccount"
    assert response.type == "FedexAccount"
    assert response.credentials["account_number"] == "123456789"
    assert response.credentials["mfa_key"] == "123456789-XXXXX"
