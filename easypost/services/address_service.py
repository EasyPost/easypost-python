from typing import (
    Any,
    Dict,
    Optional,
)

from easypost.http import HttpMethod
from easypost.models.address import (
    Address,
    AddressCollection,
)
from easypost.services.base_service import BaseService


class AddressService(BaseService):
    def __init__(self, client):
        super().__init__(client=client)

    def create(
        self,
        verify: Optional[bool] = None,
        verify_strict: Optional[bool] = None,
        **params,
    ) -> Address:
        """Create an Address."""
        endpoint = "addresses"
        method = HttpMethod.POST

        wrapped_params = {"address": params}
        if verify:
            wrapped_params["verify"] = verify
        if verify_strict:
            wrapped_params["verify_strict"] = verify_strict

        return self.request(klass=Address, method=method, endpoint=endpoint, params=wrapped_params)

    def all(self, **params) -> AddressCollection:
        """Retrieve a list of Addresses."""
        endpoint = "addresses"
        method = HttpMethod.GET

        # TODO: Store the filters

        return self.request(klass=AddressCollection, method=method, endpoint=endpoint, params=params)

    def retrieve(self, id: str) -> Address:
        """Retrieve an Address."""
        endpoint = f"addresses/{id}"
        method = HttpMethod.GET

        return self.request(klass=Address, method=method, endpoint=endpoint)

    def create_and_verify(self, **params) -> Address:
        """Create and verify an Address in one call."""
        endpoint = "addresses/create_and_verify"
        method = HttpMethod.POST

        wrapped_params = {"address": params}

        return self.request(klass=Address, method=method, endpoint=endpoint, params=wrapped_params, root_key="address")

    def verify(self, id: str) -> Address:
        """Verify an already created Address."""
        endpoint = f"addresses/{id}/verify"
        method = HttpMethod.GET

        return self.request(klass=Address, method=method, endpoint=endpoint, root_key="address")

    def get_next_page(
        self,
        addresses: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> AddressCollection:
        """Retrieve the next page of the list Addresses response."""
        self._check_has_next_page(collection=addresses)

        params = {
            "before_id": addresses["addresses"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)
