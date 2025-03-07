from typing import (
    Any,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Pickup
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class PickupService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Pickup.__name__

    def create(self, **params) -> Pickup:
        """Create a Pickup."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Pickups."""
        filters = {
            "key": "pickups",
        }

        return self._all_resources(self._model_class, filters, **params)

    def retrieve(self, id: str) -> Pickup:
        """Retrieve a Pickup."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        pickups: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Retrieve the next page of the list Pickup response."""
        self._check_has_next_page(collection=pickups)

        params = {
            "before_id": pickups["pickups"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)

    def buy(self, id: str, **params) -> Pickup:
        """Buy a Pickup."""
        url = f"{self._instance_url(self._model_class, id)}/buy"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def cancel(self, id: str, **params) -> Pickup:
        """Cancel a Pickup."""
        url = f"{self._instance_url(self._model_class, id)}/cancel"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)
