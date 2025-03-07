from typing import (
    Any,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Claim
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class ClaimService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Claim.__name__

    def create(self, **params) -> Claim:
        """Create a Claim."""
        url = "/claims"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params, beta=False)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Claims."""
        filters = {
            "key": "claims",
        }

        return self._all_resources(class_name=self._model_class, filters=filters, beta=False, **params)

    def retrieve(self, id: str) -> Claim:
        """Retrieve a Claim."""
        return self._retrieve_resource(class_name=self._model_class, id=id, beta=False)

    def get_next_page(
        self,
        claims: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Retrieve the next page of the list Claim response."""
        self._check_has_next_page(collection=claims)

        params = {
            "before_id": claims["claims"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)

    def cancel(self, id: str) -> Claim:
        """Cancel a Claim."""
        url = f"/claims/{id}/cancel"

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url=url,
            beta=False,
        )

        return convert_to_easypost_object(response=response)
