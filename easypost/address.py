from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    AllResource,
    CreateResource,
)


class Address(AllResource, CreateResource):
    @classmethod
    def create(
        cls,
        api_key: Optional[str] = None,
        verify: Optional[Union[Dict[str, Any], str, bool]] = None,
        verify_strict: Optional[Union[Dict[str, Any], str, bool]] = None,
        **params
    ) -> "Address":
        """Create an address."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()

        wrapped_params = {cls.snakecase_name(): params}  # type: Dict[str, Any]
        if verify:
            wrapped_params["verify"] = verify
        if verify_strict:
            wrapped_params["verify_strict"] = verify_strict

        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def create_and_verify(cls, api_key: Optional[str] = None, **params) -> "Address":
        """Create and verify an address."""
        requestor = Requestor(local_api_key=api_key)
        url = "%s/%s" % (cls.class_url(), "create_and_verify")

        wrapped_params = {cls.snakecase_name(): params}
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)

        response_address = response.get("address", None)

        if response_address is not None:
            verified_address = convert_to_easypost_object(response=response_address, api_key=api_key)
            return verified_address
        else:
            return convert_to_easypost_object(response=response, api_key=api_key)

    def verify(self) -> "Address":
        """Verify an address."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "verify")
        response, api_key = requestor.request(method=RequestMethod.GET, url=url)

        response_address = response.get("address", None)

        if response_address is not None:
            verified_address = convert_to_easypost_object(response=response_address, api_key=api_key)
            return verified_address
        else:
            return convert_to_easypost_object(response=response, api_key=api_key)
