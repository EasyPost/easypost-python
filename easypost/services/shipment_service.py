from typing import (
    Any,
    Optional,
)

from easypost.constant import _FILTERS_KEY
from easypost.easypost_object import convert_to_easypost_object
from easypost.models import (
    Rate,
    Shipment,
)
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService
from easypost.util import get_lowest_smart_rate


class ShipmentService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Shipment.__name__

    def create(self, **params) -> Shipment:
        """Create a Shipment."""
        url = self._class_url(self._model_class)
        wrapped_params = {
            self._snakecase_name(self._model_class): params,
        }

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Shipments."""
        filters = {
            "key": "shipments",
            "include_children": params.get("include_children"),
            "purchased": params.get("purchased"),
        }

        return self._all_resources(self._model_class, filters, **params)

    def retrieve(self, id: str) -> Shipment:
        """Retrieve a Shipment."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        shipments: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Get next page of shipment collection."""
        self._check_has_next_page(collection=shipments)

        params = {
            "before_id": shipments["shipments"][-1].id,
            "page_size": page_size,
            # Use the same include_children as the last page
            "include_children": shipments.get(_FILTERS_KEY, {}).get("include_children"),
            # Use the same purchased as the last page
            "purchased": shipments.get(_FILTERS_KEY, {}).get("purchased"),
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)

    def regenerate_rates(self, id: str) -> dict[str, list[Rate]]:
        """Regenerate Rates for a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/rerate"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url)

        return convert_to_easypost_object(response=response)

    def get_smart_rates(self, id: str) -> list[Rate]:
        """Get SmartRates for a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/smartrate"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response.get("result", []))

    def buy(
        self,
        id: str,
        end_shipper_id: Optional[str] = None,
        **params,
    ) -> Shipment:
        """Buy a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/buy"
        if end_shipper_id:
            params["end_shipper_id"] = end_shipper_id

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def refund(self, id: str, **params) -> Shipment:
        """Refund a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/refund"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def insure(self, id: str, **params) -> Shipment:
        """Insure a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/insure"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def label(self, id: str, **params) -> Shipment:
        """Convert the label format of a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/label"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def lowest_smart_rate(self, id: str, delivery_days: int, delivery_accuracy: str) -> Rate:
        """Get the lowest SmartRate of a Shipment."""
        smartrates = self.get_smart_rates(id)
        lowest_smart_rate = get_lowest_smart_rate(smartrates, delivery_days, delivery_accuracy.lower())

        return lowest_smart_rate

    def generate_form(self, id: str, form_type: str, form_options: Optional[dict[str, Any]] = {}) -> Shipment:
        """Generate a form for a Shipment."""
        params = {"type": form_type}
        params.update(form_options)  # type: ignore
        wrapped_params = {"form": params}
        url = f"{self._instance_url(self._model_class, id)}/forms"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def retrieve_estimated_delivery_date(self, id: str, planned_ship_date: str) -> list[dict[str, Any]]:
        """Retrieves the estimated delivery date of each Rate via SmartRate."""
        url = f"{self._instance_url(self._model_class, id)}/smartrate/delivery_date"
        wrapped_params = {"planned_ship_date": planned_ship_date}

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response.get("rates", []))

    def recommend_ship_date(self, id: str, desired_delivery_date: str) -> list[dict[str, Any]]:
        """Retrieve a recommended ship date for an existing Shipment via the Precision Shipping API,
        based on a specific desired delivery date.
        """
        url = f"{self._instance_url(self._model_class, id)}/smartrate/precision_shipping"
        params = {"desired_delivery_date": desired_delivery_date}
        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        return convert_to_easypost_object(response=response.get("rates", []))

    def create_and_buy_luma(
        self,
        **params: dict[str, Any],
    ) -> Shipment:
        """Create and buy a Luma Shipment in one call."""
        url = f"{self._class_url(self._model_class)}/luma"
        wrapped_params = {
            self._snakecase_name(self._model_class): params,
        }

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def buy_luma(
        self,
        id: str,
        **params: dict[str, Any],
    ) -> Shipment:
        """Buy a Shipment with Luma."""
        url = f"{self._instance_url(self._model_class, id)}/luma"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)
