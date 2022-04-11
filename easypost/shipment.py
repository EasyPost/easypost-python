from typing import List

from easypost import Rate
from easypost.error import Error
from easypost.requestor import Requestor
from easypost.resource import (
    AllResource,
    CreateResource,
)


class Shipment(AllResource, CreateResource):
    def regenerate_rates(self) -> "Shipment":
        """Regenerate rates for a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "rerate")
        response, api_key = requestor.request(method="post", url=url)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def get_smartrates(self) -> List[object]:
        """Get smartrates for a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "smartrate")
        response, api_key = requestor.request(method="get", url=url)
        return response.get("result", [])

    def buy(self, **params) -> "Shipment":
        """Buy a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request(method="post", url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def refund(self, **params) -> "Shipment":
        """Refund a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "refund")
        response, api_key = requestor.request(method="post", url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def insure(self, **params) -> "Shipment":
        """Insure a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "insure")
        response, api_key = requestor.request(method="post", url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def label(self, **params) -> "Shipment":
        """Convert the label format of a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "label")
        response, api_key = requestor.request(method="get", url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def lowest_rate(self, carriers: List[str] = None, services: List[str] = None) -> Rate:
        """Get the lowest rate of a shipment."""
        carriers = carriers or []
        services = services or []
        lowest_rate = None

        carriers = [c.lower() for c in carriers]
        services = [service.lower() for service in services]

        for rate in self.rates:
            if len(carriers) > 0 and rate.carrier.lower() not in carriers:
                continue

            if len(services) > 0 and rate.service.lower() not in services:
                continue

            if lowest_rate is None or float(rate.rate) < float(lowest_rate.rate):
                lowest_rate = rate

        if lowest_rate is None:
            raise Error(message="No rates found.")

        return lowest_rate
