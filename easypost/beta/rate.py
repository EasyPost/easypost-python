from typing import (
    Any,
    Dict,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import Resource


class Rate(Resource):
    @classmethod
    def retrieve_stateless_rates(cls, api_key: Optional[str] = None, **params) -> Dict[str, Any]:
        """Retrieves stateless rates by passing shipment data."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()
        wrapped_params = {
            "shipment": params,
        }
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params, beta=True)

        return convert_to_easypost_object(response=response.get("rates", None), api_key=api_key)
