from typing import List

from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import CreateResource
from easypost.util import get_lowest_object_rate


class Order(CreateResource):
    def get_rates(self) -> "Order":
        """Get rates for an order."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "rates")
        response, api_key = requestor.request(method=RequestMethod.GET, url=url)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def buy(self, **params) -> "Order":
        """Buy an order."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def lowest_rate(self, carriers: List[str] = None, services: List[str] = None):
        """Get the lowest rate of this order."""
        lowest_rate = get_lowest_object_rate(self, carriers, services)

        return lowest_rate
