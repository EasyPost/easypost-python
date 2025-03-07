from typing import (
    Any,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class SmartRateService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = "SmartRate"

    def estimate_delivery_date(self, **params) -> list[dict[str, Any]]:
        """Retrieve the estimated delivery date of each carrier-service level combination via the
        Smart Deliver By API, based on a specific ship date and origin-destination postal code pair.
        """
        url = "/smartrate/deliver_by"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def recommend_ship_date(self, **params) -> list[dict[str, Any]]:
        """Retrieve a recommended ship date for each carrier-service level combination via the
        Smart Deliver On API, based on a specific delivery date and origin-destination postal code pair.
        """
        url = "/smartrate/deliver_on"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)
