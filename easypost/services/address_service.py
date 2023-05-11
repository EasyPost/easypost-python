from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models.address import Address
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class AddressService(BaseService):
    def create(
        self,
        verify: Optional[Union[Dict[str, Any], str, bool]] = None,
        verify_strict: Optional[Union[Dict[str, Any], str, bool]] = None,
        **params,
    ) -> Address:
        """Create an Address."""
        url = self.class_url("address")

        wrapped_params = {self.snakecase_name("address"): params}  # type: Dict[str, Any]
        if verify:
            wrapped_params["verify"] = verify
        if verify_strict:
            wrapped_params["verify_strict"] = verify_strict

        response, api_key = Requestor().request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response, api_key=api_key)

    def all(self, **params) -> List[Any]:
        """Retrieve a list of Addresses."""
        return self.all_resources("address", **params)

    def retrieve(self, id) -> Address:
        """Retrieve an Address."""
        return self.retrieve_resource("address", id)

    def create_and_verify(self, **params) -> Address:
        """Create and verify an Address."""
        url = f"{self.class_url('address')}/create_and_verify"
        wrapped_params = {self.snakecase_name("address"): params}

        response, api_key = Requestor().request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response["address"], api_key=api_key)

    def verify(self, id) -> Address:
        """Verify an address."""
        url = f"{self.instance_url('address', id)}/verify"

        response, api_key = Requestor().request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response["address"], api_key=api_key)

    def get_next_page(
        self,
        collection: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        return self.get_next_page_resources("address", collection, page_size, optional_params)
