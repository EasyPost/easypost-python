from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models.pickup import Pickup
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

    def all(self, **params) -> List[Pickup]:
        """Retrieve a list of Pickups."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id) -> Pickup:
        """Retrieve a Pickup."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        pickups: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> List[Pickup]:
        """Retrieve the next page of the list Pickup response."""
        return self._get_next_page_resources(self._model_class, pickups, page_size, optional_params)

    def buy(self, id: str, **params) -> Pickup:
        """Buy a Pickup."""
        url = f"{self._instance_url(self._model_class, id)}/buy"

        response, api_key = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response, api_key=api_key)

    def cancel(self, id: str, **params) -> Pickup:
        """Cancel a Pickup."""
        url = f"{self._instance_url(self._model_class, id)}/cancel"

        response, api_key = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response, api_key=api_key)
