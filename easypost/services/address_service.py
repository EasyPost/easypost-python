from typing import (
    Any,
    Dict,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Address
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class AddressService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Address.__name__

    def create(
        self,
        verify: Optional[bool] = None,
        verify_strict: Optional[bool] = None,
        **params,
    ) -> Address:
        """Create an Address."""
        url = self._class_url(self._model_class)
        wrapped_params = {self._snakecase_name(self._model_class): params}  # type: Dict[str, Any]

        if verify:
            wrapped_params["verify"] = verify
        if verify_strict:
            wrapped_params["verify_strict"] = verify_strict

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of Addresses."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id) -> Address:
        """Retrieve an Address."""
        return self._retrieve_resource(self._model_class, id)

    def create_and_verify(self, **params) -> Address:
        """Create and verify an Address in one call."""
        url = f"{self._class_url('address')}/create_and_verify"
        wrapped_params = {self._snakecase_name(self._model_class): params}

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response["address"])

    def verify(self, id) -> Address:
        """Verify an already created Address."""
        url = f"{self._instance_url('address', id)}/verify"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response["address"])

    def get_next_page(
        self,
        addresses: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve the next page of the list Addresses response."""
        return self._get_next_page_resources(self._model_class, addresses, page_size, optional_params)
