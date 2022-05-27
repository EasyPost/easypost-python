from typing import (
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    CreateResource,
    DeleteResource,
    UpdateResource,
)


class User(CreateResource, UpdateResource, DeleteResource):
    @classmethod
    def create(cls, api_key: Optional[str] = None, **params) -> "User":
        """Create a child user."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()
        wrapped_params = {cls.snakecase_name(): params}
        response, api_key = requestor.request(
            method=RequestMethod.POST,
            url=url,
            params=wrapped_params,
        )
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def retrieve(cls, easypost_id: Optional[str] = None, api_key: Optional[str] = None, **params) -> "User":
        """Retrieve a user."""
        if not easypost_id:
            requestor = Requestor(local_api_key=api_key)
            response, api_key = requestor.request(method=RequestMethod.GET, url=cls.class_url())
            return convert_to_easypost_object(response=response, api_key=api_key)
        else:
            instance = cls(easypost_id=easypost_id, api_key=api_key, **params)
            instance.refresh()
            return instance

    @classmethod
    def retrieve_me(cls, api_key: Optional[str] = None, **params) -> "User":
        """Retrieve the authenticated user."""
        requestor = Requestor(local_api_key=api_key)
        response, api_key = requestor.request(method=RequestMethod.GET, url=cls.class_url())
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def all_api_keys(cls, api_key: Optional[str] = None) -> "User":
        """Get all API keys including child user keys."""
        requestor = Requestor(local_api_key=api_key)
        url = "/api_keys"
        response, api_key = requestor.request(method=RequestMethod.GET, url=url)
        return convert_to_easypost_object(response=response, api_key=api_key)

    def api_keys(self) -> List[str]:
        """Get the authenticated user's API keys."""
        api_keys = self.all_api_keys()

        if api_keys.id == self.id:
            return api_keys.keys
        else:
            for child in api_keys.children:
                if child.id == self.id:
                    return child.keys

        return []

    def update_brand(self, api_key: Optional[str] = None, **params) -> "User":
        """Update the User's Brand."""
        requestor = Requestor(local_api_key=api_key)
        response, api_key = requestor.request(
            method=RequestMethod.PATCH, url=self.instance_url() + "/brand", params=params
        )
        return convert_to_easypost_object(response=response, api_key=api_key)
