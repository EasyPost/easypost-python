from typing import Optional

from easypost.easypost_object import convert_to_easypost_object
from easypost.error import Error
from easypost.payment_method import PaymentMethod
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    CreateResource,
    Resource,
)


class CreditCard(CreateResource, Resource):
    @classmethod
    def fund(cls, amount: str, primary_or_secondary: str = "primary", api_key: Optional[str] = None) -> "CreditCard":
        """Fund your EasyPost wallet by charging your primary or secondary card on file."""
        payment_methods = PaymentMethod.all()

        payment_method_map = {
            "primary": "primary_payment_method",
            "secondary": "secondary_payment_method",
        }

        payment_method_to_use = payment_method_map.get(primary_or_secondary)
        card_id = payment_methods[payment_method_to_use]["id"] if payment_method_to_use else None

        if payment_method_to_use is None or card_id is None or "card_" not in card_id:
            raise Error(message="The chosen payment method is not a credit card. Please try again.")

        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{card_id}/charges"
        wrapped_params = {"amount": amount}
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def delete(cls, credit_card_id: str, api_key: Optional[str] = None):
        """Delete a credit card by ID."""
        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{credit_card_id}"
        response, api_key = requestor.request(method=RequestMethod.DELETE, url=url)
        return convert_to_easypost_object(response=response, api_key=api_key)
