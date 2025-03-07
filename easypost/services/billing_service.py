from typing import (
    Any,
)

from easypost.constant import (
    INVALID_PAYMENT_METHOD_ERROR,
    NO_BILLING_ERROR,
)
from easypost.easypost_object import convert_to_easypost_object
from easypost.errors import InvalidObjectError
from easypost.models import Billing
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class BillingService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Billing.__name__

    def fund_wallet(self, amount: str, priority: str = "primary") -> None:
        """Fund your EasyPost wallet by charging your primary or secondary payment method on file."""
        endpoint, payment_method_id = self._get_payment_method_info(priority=priority)

        url = f"{endpoint}/{payment_method_id}/charges"
        wrapped_params = {"amount": amount}

        Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

    def delete_payment_method(self, priority: str) -> None:
        """Delete a payment method."""
        endpoint, payment_method_id = self._get_payment_method_info(priority=priority)

        url = f"{endpoint}/{payment_method_id}"

        Requestor(self._client).request(method=RequestMethod.DELETE, url=url)

    def retrieve_payment_methods(self, **params) -> dict[str, Any]:
        """Retrieve payment methods."""
        response = Requestor(self._client).request(
            method=RequestMethod.GET,
            url="/payment_methods",
            params=params,
        )

        if response.get("id") is None:
            raise InvalidObjectError(message=NO_BILLING_ERROR)

        return convert_to_easypost_object(response=response)

    def _get_payment_method_info(self, priority: str = "primary") -> list[str]:
        """Get payment method info (type of the payment method and ID of the payment method)"""
        payment_methods = self.retrieve_payment_methods()

        payment_method_map = {
            "primary": "primary_payment_method",
            "secondary": "secondary_payment_method",
        }

        payment_method_to_use = payment_method_map.get(priority)

        if payment_method_to_use and payment_methods[payment_method_to_use]:
            payment_method_id = payment_methods[payment_method_to_use]["id"]
            payment_method_object_type = payment_methods[payment_method_to_use].get("object", None)
            if payment_method_object_type == "CreditCard":
                endpoint = "/credit_cards"
            elif payment_method_object_type == "BankAccount":
                endpoint = "/bank_accounts"
            else:
                raise InvalidObjectError(message=INVALID_PAYMENT_METHOD_ERROR)
        else:
            raise InvalidObjectError(message=INVALID_PAYMENT_METHOD_ERROR)

        return [endpoint, payment_method_id]
