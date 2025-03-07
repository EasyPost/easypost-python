from typing import (
    Any,
    Optional,
)

from easypost.models import ScanForm
from easypost.services.base_service import BaseService


class ScanFormService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = ScanForm.__name__

    def create(self, **params) -> ScanForm:
        """Create a ScanForm."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of ScanForms."""
        filters = {
            "key": "scan_forms",
        }

        return self._all_resources(self._model_class, filters, **params)

    def retrieve(self, id: str) -> ScanForm:
        """Retrieve a ScanForm."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        scan_forms: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Retrieve the next page of the list ScanForm response."""
        self._check_has_next_page(collection=scan_forms)

        params = {
            "before_id": scan_forms["scan_forms"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)
