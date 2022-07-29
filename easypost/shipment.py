from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost import Rate
from easypost.easypost_object import convert_to_easypost_object
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
    @classmethod
    def create(cls, api_key: Optional[str] = None, with_carbon_offset: Optional[bool] = False, **params) -> "Shipment":
        """Create an Shipment object."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()
        wrapped_params = {
            cls.snakecase_name(): params,
            "carbon_offset": with_carbon_offset,
        }
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    def regenerate_rates(self, with_carbon_offset: Optional[bool] = False) -> "Shipment":
        """Regenerate rates for a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "rerate")
        params = {
            "carbon_offset": with_carbon_offset,
        }
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def get_smartrates(self) -> List[object]:
        """Get smartrates for a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "smartrate")
        response, _ = requestor.request(method=RequestMethod.GET, url=url)
        return response.get("result", [])

    def buy(self, with_carbon_offset: Optional[bool] = False, **params) -> "Shipment":
        """Buy a shipment."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        params["carbon_offset"] = with_carbon_offset

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
        lowest_smartrate = self.get_lowest_smartrate(smartrates, delivery_days, delivery_accuracy.lower())

        return lowest_smartrate

    def generate_form(self, form_type: str, form_options: Optional[Dict[str, Any]] = {}) -> "Shipment":
        """Generate a form for a Shipment."""
        params = {"type": form_type}
        params.update(form_options)  # type: ignore
        wrapped_params = {"form": params}

        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "forms")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        self.refresh_from(values=response, api_key=api_key)
        return self

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
