from typing import (
    Any,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Insurance
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class InsuranceService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Insurance.__name__

    def create(self, **params) -> Insurance:
        """Create an Insurance."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Insurances."""
        filters = {
            "key": "insurances",
        }

        return self._all_resources(self._model_class, filters, **params)

    def retrieve(self, id: str) -> Insurance:
        """Retrieve an Insurance."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        insurances: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Retrieve the next page of the list Insurance response."""
        self._check_has_next_page(collection=insurances)

        params = {
            "before_id": insurances["insurances"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)

    def refund(self, id: str) -> Insurance:
        url = f"/insurances/{id}/refund"
        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url=url,
        )

        return convert_to_easypost_object(response=response)
