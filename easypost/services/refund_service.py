from typing import (
    Any,
    Optional,
)

from easypost.models import Refund
from easypost.services.base_service import BaseService


class RefundService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Refund.__name__

    def create(self, **params) -> Refund:
        """Create a Shipment Refund."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Shipment Refunds."""
        filters = {
            "key": "refunds",
        }

        return self._all_resources(self._model_class, filters, **params)

    def retrieve(self, id: str) -> Refund:
        """Retrieve a Shipment Refund."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        refunds: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Retrieve the next page of the list Refund response."""
        self._check_has_next_page(collection=refunds)

        params = {
            "before_id": refunds["refunds"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)
