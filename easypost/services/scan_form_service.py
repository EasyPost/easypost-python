from typing import (
    Any,
    Dict,
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

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of ScanForms."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id: str) -> ScanForm:
        """Retrieve a ScanForm."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        scan_forms: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve the next page of the list ScanForm response."""
        return self._get_next_page_resources(self._model_class, scan_forms, page_size, optional_params)
