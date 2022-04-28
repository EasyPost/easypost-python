from typing import List

from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import CreateResource
from easypost.util import get_lowest_object_rate


class Pickup(CreateResource):
    def buy(self, **params) -> "Pickup":
        """Buy a pickup."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def cancel(self, **params) -> "Pickup":
        """Cancel a pickup."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "cancel")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def lowest_rate(self, carriers: List[str] = None, services: List[str] = None):
        """Get the lowest rate of this pickup."""
        lowest_rate = get_lowest_object_rate(self, carriers, services, "pickup_rates")

        return lowest_rate
