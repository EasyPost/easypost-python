from typing import (
    Any,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import (
    Address,
    EndShipper,
)
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class EndShipperService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Address.__name__
        self._service_class = EndShipper.__name__

    def create(self, **params) -> Address:
        """Create an EndShipper."""
        url = self._class_url(self._service_class)
        wrapped_params = {self._snakecase_name(self._model_class): params}

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of EndShippers."""
        return self._all_resources(self._service_class, **params)

    def retrieve(self, id: str) -> Address:
        """Retrieve an EndShipper."""
        return self._retrieve_resource(self._service_class, id)

    def update(self, id: str, **params) -> Address:
        """Update an EndShipper object.

        This function requires all parameters to be present for an EndShipper.
        """
        url = self._instance_url(self._service_class, id)
        wrapped_params = {self._snakecase_name(self._model_class): params}

        response = Requestor(self._client).request(method=RequestMethod.PUT, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)
