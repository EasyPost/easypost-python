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
    def fund(cls, api_key: Optional[str] = None, **params) -> "CreditCard":
        """Fund your EasyPost wallet by charging your primary or secondary card on file."""
        payment_methods = PaymentMethod.all()

        payment_method_map = {
            "primary": "primary_payment_method",
            "secondary": "secondary_payment_method",
        }

        primary_or_secondary = params.get("primary_or_secondary")
        payment_method_to_use = payment_method_map.get(primary_or_secondary) if primary_or_secondary else None

        if (
            payment_method_to_use is None
            or payment_methods[payment_method_to_use] is None
            or "card_" not in payment_methods[payment_method_to_use].get("id")
        ):
            raise Error(message="The chosen payment method is not a credit card. Please try again.")

        card_id = payment_method_to_use.get("id")

        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{card_id}/charges"
        wrapped_params = {"amount": params.get("amount")}
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def delete(cls, easypost_id: str, api_key: Optional[str] = None):
        """Delete a credit card by ID."""
        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{easypost_id}"
        response, api_key = requestor.request(method=RequestMethod.DELETE, url=url)
        return convert_to_easypost_object(response=response, api_key=api_key)
