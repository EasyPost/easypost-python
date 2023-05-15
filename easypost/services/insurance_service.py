from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.models.insurance import Insurance
from easypost.services.base_service import BaseService


class InsuranceService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Insurance.__name__

    def create(self, **params) -> Insurance:
        """Create an Insurance."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> List[Insurance]:
        """Retrieve a list of Insurances."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id) -> Insurance:
        """Retrieve an Insurance."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        insurances: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Retrieve the next page of the List Insurance response."""
        return self._get_next_page_resources(self._model_class, insurances, page_size, optional_params)
