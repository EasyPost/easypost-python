from typing import (
    Any,
    Dict,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.error import Error
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import Resource


class PaymentMethod(Resource):
    @classmethod
    def all(cls, api_key: Optional[str] = None, **params) -> Dict[str, Any]:
        """Retrieve a list of payment methods."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)

        if response.get("id") is None:
            raise Error(message="Billing has not been setup for this user. Please add a payment method.")

        return convert_to_easypost_object(response=response, api_key=api_key)
