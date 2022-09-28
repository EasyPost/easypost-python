from typing import Optional

from easypost.easypost_object import (
    EasyPostObject,
    convert_to_easypost_object,
)
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import AllResource


class EndShipper(AllResource):
    @classmethod
    def create(cls, api_key: Optional[str] = None, **params) -> "EndShipper":
        """Create an EndShipper."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()
        wrapped_params = {"address": params}
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    def save(self) -> "EndShipper":
        """Update an EndShipper object.

        This function requires all parameters to be present for an EndShipper.
        """
        if self._unsaved_values:
            requestor = Requestor(local_api_key=self._api_key)
            params = {}
            for k in self._unsaved_values:
                params[k] = getattr(self, k)
                if type(params[k]) is EasyPostObject:
                    params[k] = params[k].flatten_unsaved()
            wrapped_params = {"address": params}  # This function is overridden due to the key has to be `address`
            url = self.instance_url()
            response, api_key = requestor.request(method=RequestMethod.PUT, url=url, params=wrapped_params)
            self.refresh_from(values=response, api_key=api_key)

        return self
