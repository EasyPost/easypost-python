from typing import (
    Any,
    Dict,
    List,
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

    def all(self, **params) -> List[Refund]:
        """Retrieve a list of Shipment Refunds."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id: str) -> Refund:
        """Retrieve a Shipment Refund."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        refunds: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve the next page of the list Refund response."""
        return self._get_next_page_resources(self._model_class, refunds, page_size, optional_params)
