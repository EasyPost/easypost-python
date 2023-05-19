from typing import (
    Any,
    Dict,
    List,
    Optional,
)

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

    def create(self, with_carbon_offset: Optional[bool] = False, **params) -> Shipment:
        """Create a Shipment."""
        url = self._class_url(self._model_class)
        wrapped_params = {
            self._snakecase_name(self._model_class): params,
            "carbon_offset": with_carbon_offset,
        }

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of Shipments."""
        response = Requestor(self._client).request(method=RequestMethod.GET, url="/shipments", params=params)
        response["include_children"] = params.get("include_children")
        response["purchased"] = params.get("purchased")

        return convert_to_easypost_object(response=response)

    def retrieve(self, id: str) -> Shipment:
        """Retrieve a Shipment."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        shipments: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Get next page of shipment collection."""
        optional_params = {
            "include_children": shipments.get("include_children"),
            "purchased": shipments.get("purchased"),
        }

        return self._get_next_page_resources(self._model_class, shipments, page_size, optional_params)

    def regenerate_rates(self, id: str, with_carbon_offset: Optional[bool] = False) -> Shipment:
        """Regenerate Rates for a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/rerate"
        wrapped_params = {"carbon_offset": with_carbon_offset}

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def get_smart_rates(self, id: str) -> List[Rate]:
        """Get SmartRates for a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/smartrate"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response.get("result", []))

    def buy(
        self,
        id: str,
        with_carbon_offset: Optional[bool] = False,
        end_shipper_id: Optional[str] = None,
        **params,
    ) -> Shipment:
        """Buy a Shipment."""
        url = f"{self._instance_url(self._model_class, id)}/buy"
        params["carbon_offset"] = with_carbon_offset
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

    def generate_form(self, id: str, form_type: str, form_options: Optional[Dict[str, Any]] = {}) -> Shipment:
        """Generate a form for a Shipment."""
        params = {"type": form_type}
        params.update(form_options)  # type: ignore
        wrapped_params = {"form": params}
        url = f"{self._instance_url(self._model_class, id)}/forms"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def retrieve_estimated_delivery_date(self, id: str, planned_ship_date: str) -> List[Dict[str, Any]]:
        """Retrieves the estimated delivery date of each Rate via SmartRate."""
        url = f"{self._instance_url(self._model_class, id)}/smartrate/delivery_date"
        wrapped_params = {"planned_ship_date": planned_ship_date}

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response.get("rates", []))
