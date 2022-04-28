from typing import List

from easypost import Rate
from easypost.error import Error
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    AllResource,
    CreateResource,
)
from easypost.util import get_lowest_object_rate


class Shipment(AllResource, CreateResource):
    def regenerate_rates(self) -> "Shipment":
        """Regenerate rates for a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "rerate")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def get_smartrates(self) -> List[object]:
        """Get smartrates for a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "smartrate")
        response, _ = requestor.request(method=RequestMethod.GET, url=url)
        return response.get("result", [])

    def buy(self, **params) -> "Shipment":
        """Buy a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def refund(self, **params) -> "Shipment":
        """Refund a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "refund")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def insure(self, **params) -> "Shipment":
        """Insure a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "insure")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def label(self, **params) -> "Shipment":
        """Convert the label format of a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "label")
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def lowest_rate(self, carriers: List[str] = None, services: List[str] = None) -> Rate:
        """Get the lowest rate of this shipment."""
        lowest_rate = get_lowest_object_rate(self, carriers, services)

        return lowest_rate

    def lowest_smartrate(self, delivery_days: int, delivery_accuracy: str) -> Rate:
        """Get the lowest smartrate of this shipment."""
        smartrates = self.get_smartrates()
        lowest_smartrate = self.get_lowest_smartrate(smartrates, delivery_days, delivery_accuracy)

        return lowest_smartrate

    @staticmethod
    def get_lowest_smartrate(smartrates, delivery_days: int, delivery_accuracy: str) -> Rate:
        """Get the lowest smartrate from a list of smartrates."""
        valid_delivery_accuracy_values = {
            "percentile_50",
            "percentile_75",
            "percentile_85",
            "percentile_90",
            "percentile_95",
            "percentile_97",
            "percentile_99",
        }
        lowest_smartrate = None

        if delivery_accuracy.lower() not in valid_delivery_accuracy_values:
            raise Error(message=f"Invalid delivery_accuracy value, must be one of: {valid_delivery_accuracy_values}")

        for rate in smartrates:
            if rate["time_in_transit"][delivery_accuracy] > delivery_days:
                continue
            elif lowest_smartrate is None or float(rate["rate"]) < float(lowest_smartrate["rate"]):
                lowest_smartrate = rate

        if lowest_smartrate is None:
            raise Error(message="No rates found.")

        return lowest_smartrate
