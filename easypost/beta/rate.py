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

    @classmethod
    def get_lowest_stateless_rate(
        cls, stateless_rates: List[Dict[str, Any]], carriers: List[str] = None, services: List[str] = None
    ) -> Dict[str, Any]:
        """Get the lowest stateless rate."""
        carriers = carriers or []
        services = services or []
        lowest_rate = None

        carriers = [carrier.lower() for carrier in carriers]
        services = [service.lower() for service in services]

        for rate in stateless_rates:
            if (carriers and rate["carrier"].lower() not in carriers) or (
                services and rate["service"].lower() not in services
            ):
                continue

            if lowest_rate is None or float(rate.rate) < float(lowest_rate.rate):
                lowest_rate = rate

        if lowest_rate is None:
            raise Error(message="No rates found.")

        return lowest_rate
