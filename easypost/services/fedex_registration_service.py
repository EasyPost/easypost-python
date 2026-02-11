import uuid
from typing import Any

from easypost.easypost_object import convert_to_easypost_object
from easypost.models.fedex_account_validation_response import FedExAccountValidationResponse
from easypost.models.fedex_request_pin_response import FedExRequestPinResponse
from easypost.requestor import RequestMethod, Requestor
from easypost.services.base_service import BaseService


class FedExRegistrationService(BaseService):
    def __init__(self, client):
        self._client = client

    def register_address(self, fedex_account_number: str, **params) -> FedExAccountValidationResponse:
        """Register the billing address for a FedEx account.

        Args:
            fedex_account_number: The FedEx account number.
            params: Map of parameters.

        Returns:
            FedExAccountValidationResponse object with next steps (PIN or invoice validation).
        """
        wrapped_params = self._wrap_address_validation(params)
        url = f"/fedex_registrations/{fedex_account_number}/address"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def request_pin(self, fedex_account_number: str, pin_method_option: str) -> FedExRequestPinResponse:
        """Request a PIN for FedEx account verification.

        Args:
            fedex_account_number: The FedEx account number.
            pin_method_option: The PIN delivery method: "SMS", "CALL", or "EMAIL".

        Returns:
            FedExRequestPinResponse object confirming PIN was sent.
        """
        wrapped_params = {"pin_method": {"option": pin_method_option}}
        url = f"/fedex_registrations/{fedex_account_number}/pin"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def validate_pin(self, fedex_account_number: str, **params) -> FedExAccountValidationResponse:
        """Validate the PIN entered by the user for FedEx account verification.

        Args:
            fedex_account_number: The FedEx account number.
            params: Map of parameters.

        Returns:
            FedExAccountValidationResponse object.
        """
        wrapped_params = self._wrap_pin_validation(params)
        url = f"/fedex_registrations/{fedex_account_number}/pin/validate"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def submit_invoice(self, fedex_account_number: str, **params) -> FedExAccountValidationResponse:
        """Submit invoice information to complete FedEx account registration.

        Args:
            fedex_account_number: The FedEx account number.
            params: Map of parameters.

        Returns:
            FedExAccountValidationResponse object.
        """
        wrapped_params = self._wrap_invoice_validation(params)
        url = f"/fedex_registrations/{fedex_account_number}/invoice"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def _wrap_address_validation(self, params: dict[str, Any]) -> dict[str, Any]:
        """Wraps address validation parameters and ensures the "name" field exists.
        If not present, generates a UUID (with hyphens removed) as the name.

        Args:
            params: The original parameters map.

        Returns:
            A new map with properly wrapped address_validation and easypost_details.
        """
        wrapped_params = {}

        if "address_validation" in params:
            address_validation = params["address_validation"].copy()
            self._ensure_name_field(address_validation)
            wrapped_params["address_validation"] = address_validation

        if "easypost_details" in params:
            wrapped_params["easypost_details"] = params["easypost_details"]

        return wrapped_params

    def _wrap_pin_validation(self, params: dict[str, Any]) -> dict[str, Any]:
        """Wraps PIN validation parameters and ensures the "name" field exists.
        If not present, generates a UUID (with hyphens removed) as the name.

        Args:
            params: The original parameters map.

        Returns:
            A new map with properly wrapped pin_validation and easypost_details.
        """
        wrapped_params = {}

        if "pin_validation" in params:
            pin_validation = params["pin_validation"].copy()
            self._ensure_name_field(pin_validation)
            wrapped_params["pin_validation"] = pin_validation

        if "easypost_details" in params:
            wrapped_params["easypost_details"] = params["easypost_details"]

        return wrapped_params

    def _wrap_invoice_validation(self, params: dict[str, Any]) -> dict[str, Any]:
        """Wraps invoice validation parameters and ensures the "name" field exists.
        If not present, generates a UUID (with hyphens removed) as the name.

        Args:
            params: The original parameters map.

        Returns:
            A new map with properly wrapped invoice_validation and easypost_details.
        """
        wrapped_params = {}

        if "invoice_validation" in params:
            invoice_validation = params["invoice_validation"].copy()
            self._ensure_name_field(invoice_validation)
            wrapped_params["invoice_validation"] = invoice_validation

        if "easypost_details" in params:
            wrapped_params["easypost_details"] = params["easypost_details"]

        return wrapped_params

    def _ensure_name_field(self, mapping: dict[str, Any]) -> None:
        """Ensures the "name" field exists in the provided map.
        If not present, generates a UUID (with hyphens removed) as the name.
        This follows the pattern used in the web UI implementation.

        Args:
            mapping: The map to ensure the "name" field in.
        """
        if "name" not in mapping or mapping["name"] is None:
            mapping["name"] = str(uuid.uuid4()).replace("-", "")
