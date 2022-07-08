from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.error import Error
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    CreateResource,
    Resource,
)


class Billing(CreateResource, Resource):
    @classmethod
    def fund_wallet(cls, amount: str, primary_or_secondary: str = "primary", api_key: Optional[str] = None) -> bool:
        """Fund your EasyPost wallet by charging your primary or secondary payment method on file."""
        endpoint, payment_method_id = Billing._get_payment_method_info(primary_or_secondary=primary_or_secondary)

        requestor = Requestor(local_api_key=api_key)
        url = f"{endpoint}/{payment_method_id}/charges"
        wrapped_params = {"amount": amount}
        requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)

        # Return true if the request succeeds, an error will be thrown if it fails
        return True

    @classmethod
    def delete_payment_method(cls, primary_or_secondary: str, api_key: Optional[str] = None) -> bool:
        """Delete a payment method."""
        endpoint, payment_method_id = Billing._get_payment_method_info(primary_or_secondary=primary_or_secondary)

        requestor = Requestor(local_api_key=api_key)
        url = f"{endpoint}/{payment_method_id}"
        requestor.request(method=RequestMethod.DELETE, url=url)

        # Return true if the request succeeds, an error will be thrown if it fails
        return True

    @classmethod
    def retrieve_payment_methods(cls, api_key: Optional[str] = None, **params) -> Dict[str, Any]:
        """Retrieve payment methods."""
        requestor = Requestor(local_api_key=api_key)
        response, api_key = requestor.request(method=RequestMethod.GET, url="/payment_methods", params=params)

        if response.get("id") is None:
            raise Error(message="Billing has not been setup for this user. Please add a payment method.")

        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def _get_payment_method_info(cls, primary_or_secondary: str = "primary") -> List[str]:
        """Get payment method info (type of the payment method and ID of the payment method)"""
        payment_methods = Billing.retrieve_payment_methods()

        payment_method_map = {
            "primary": "primary_payment_method",
            "secondary": "secondary_payment_method",
        }

        payment_method_to_use = payment_method_map.get(primary_or_secondary)
        error_string = "The chosen payment method is not valid. Please try again."

        if payment_method_to_use and payment_methods[payment_method_to_use]:
            payment_method_id = payment_methods[payment_method_to_use]["id"]
            if payment_method_id.startswith("card_"):
                endpoint = "/credit_cards"
            elif payment_method_id.startswith("bank_"):
                endpoint = "/bank_accounts"
            else:
                raise Error(message=error_string)
        else:
            raise Error(message=error_string)

        return [endpoint, payment_method_id]
