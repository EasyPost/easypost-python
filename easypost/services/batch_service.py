from typing import (
    Any,
    Dict,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Batch
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class BatchService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Batch.__name__

    def create(self, **params) -> Batch:
        """Create a Batch."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of Batches."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id: str) -> Batch:
        """Retrieve a Batch."""
        return self._retrieve_resource(self._model_class, id)

    def create_and_buy(self, **params) -> Batch:
        """Create and buy a Batch in a single call."""
        url = f"{self._class_url(self._model_class)}/create_and_buy"
        wrapped_params = {self._snakecase_name(self._model_class): params}

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def buy(self, id: str, **params) -> Batch:
        """Buy a Batch."""
        url = f"{self._instance_url(self._model_class, id)}/buy"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def label(self, id: str, **params) -> Batch:
        """Create a Batch label."""
        url = f"{self._instance_url(self._model_class, id)}/label"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def remove_shipments(self, id: str, **params) -> Batch:
        """Remove Shipments from a Batch."""
        url = f"{self._instance_url(self._model_class, id)}/remove_shipments"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def add_shipments(self, id: str, **params) -> Batch:
        """Add Shipments to a Batch."""
        url = f"{self._instance_url(self._model_class, id)}/add_shipments"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def create_scan_form(self, id: str, **params) -> Batch:
        """Create a ScanForm for a Batch."""
        url = f"{self._instance_url(self._model_class, id)}/scan_form"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def get_next_page(
        self,
        batches: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve the next page of the list Batch response."""
        return self._get_next_page_resources(self._model_class, batches, page_size, optional_params)
