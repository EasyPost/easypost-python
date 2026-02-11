import uuid
from typing import Any

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import RequestMethod, Requestor
from easypost.services.base_service import BaseService


class FedExRegistrationService(BaseService):
    def __init__(self, client):
        self._client = client

    def register_address(self, fedex_account_number: str, **params) -> dict[str, Any]:
        """Register the billing address for a FedEx account."""
        wrapped_params = self._wrap_address_validation(params)
        url = f"/fedex_registrations/{fedex_account_number}/address"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def request_pin(self, fedex_account_number: str, pin_method_option: str) -> dict[str, Any]:
        """Request a PIN for FedEx account verification."""
        wrapped_params = {"pin_method": {"option": pin_method_option}}
        url = f"/fedex_registrations/{fedex_account_number}/pin"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def validate_pin(self, fedex_account_number: str, **params) -> dict[str, Any]:
        """Validate the PIN entered by the user for FedEx account verification."""
        wrapped_params = self._wrap_pin_validation(params)
        url = f"/fedex_registrations/{fedex_account_number}/pin/validate"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def submit_invoice(self, fedex_account_number: str, **params) -> dict[str, Any]:
        """Submit invoice information to complete FedEx account registration."""
        wrapped_params = self._wrap_invoice_validation(params)
        url = f"/fedex_registrations/{fedex_account_number}/invoice"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def _wrap_address_validation(self, params: dict[str, Any]) -> dict[str, Any]:
        """Wraps address validation parameters and ensures the "name" field exists.
        If not present, generates a UUID (with hyphens removed) as the name.
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
        """
        if "name" not in mapping or mapping["name"] is None:
            mapping["name"] = str(uuid.uuid4()).replace("-", "")
