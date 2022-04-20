from typing import (
    Any,
    Dict,
    Optional,
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
        verify: Optional[Dict[str, Any]] = None,
        verify_strict: Dict[str, Any] = None,
        **params
    ) -> "Address":
        """Create an address."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()

        wrapped_params = {cls.snakecase_name(): params}
        for key, value in (("verify", verify), ("verify_strict", verify_strict)):
            if not value:
                continue
            elif isinstance(value, (bool, str)):
                value = [value]
            wrapped_params[key] = value

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

    def verify(self, carrier: Optional[str] = None) -> "Address":
        """Verify an address."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "verify")
        params = {"carrier": carrier}
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)

        response_address = response.get("address", None)
        response_message = response.get("message", None)

        if response_address is not None:
            verified_address = convert_to_easypost_object(response=response_address, api_key=api_key)
            if response_message is not None:
                verified_address.message = response_message
                verified_address._immutable_values.update("message")
            return verified_address
        else:
            return convert_to_easypost_object(response=response, api_key=api_key)
