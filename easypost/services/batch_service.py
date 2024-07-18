from typing import (
    Any,
    Dict,
    Optional,
)

from easypost.http import HttpMethod
from easypost.models.batch import (
    Batch,
    BatchCollection,
)
from easypost.services.base_service import BaseService


class BatchService(BaseService):
    def __init__(self, client):
        super().__init__(client=client)

    def create(self, **params) -> Batch:
        """Create a Batch."""
        endpoint = "batches"
        method = HttpMethod.POST

        return self.request(klass=Batch, method=method, endpoint=endpoint, params=params)

    def all(self, **params) -> BatchCollection:
        """Retrieve a list of Batches."""
        endpoint = "batches"
        method = HttpMethod.GET

        # TODO: Store the filters

        return self.request(klass=BatchCollection, method=method, endpoint=endpoint, params=params)

    def retrieve(self, id: str) -> Batch:
        """Retrieve a Batch."""
        endpoint = f"batches/{id}"
        method = HttpMethod.GET

        return self.request(klass=Batch, method=method, endpoint=endpoint)

    def buy(self, id: str, **params) -> Batch:
        """Buy a Batch."""
        endpoint = f"batches/{id}/buy"
        method = HttpMethod.POST

        return self.request(klass=Batch, method=method, endpoint=endpoint, params=params)

    def label(self, id: str, **params) -> Batch:
        """Create a Batch label."""
        endpoint = f"batches/{id}/label"
        method = HttpMethod.POST

        return self.request(klass=Batch, method=method, endpoint=endpoint, params=params)

    def remove_shipments(self, id: str, **params) -> Batch:
        """Remove Shipments from a Batch."""
        endpoint = f"batches/{id}/remove_shipments"
        method = HttpMethod.POST

        return self.request(klass=Batch, method=method, endpoint=endpoint, params=params)

    def add_shipments(self, id: str, **params) -> Batch:
        """Add Shipments to a Batch."""
        endpoint = f"batches/{id}/add_shipments"
        method = HttpMethod.POST

        return self.request(klass=Batch, method=method, endpoint=endpoint, params=params)

    def create_scan_form(self, id: str, **params) -> Batch:
        """Create a ScanForm for a Batch."""
        endpoint = f"batches/{id}/scan_form"
        method = HttpMethod.POST

        return self.request(klass=Batch, method=method, endpoint=endpoint, params=params)

    def get_next_page(
        self,
        batches: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> BatchCollection:
        """
        Retrieve the next page of the list Batch response.

        NOTE: This function has known issues with retrieving pages in order due to server-side issues.
        It is not recommended to be used currently.
        """
        # API doesn't return batches newest to oldest, so these parameters don't work as expected
        self._check_has_next_page(collection=batches)

        params = {
            "before_id": batches["batches"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)
