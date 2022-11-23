from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.api_key import ApiKey
from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    DeleteResource,
    UpdateResource,
)


class User(UpdateResource, DeleteResource):
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
    def all_api_keys(cls, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve a list of all API keys."""
        requestor = Requestor(local_api_key=api_key)
        url = "/api_keys"
        response, api_key = requestor.request(method=RequestMethod.GET, url=url)
        return convert_to_easypost_object(response=response, api_key=api_key)

    def api_keys(self) -> List[ApiKey]:
        """Retrieve a list of API keys (works for the authenticated user or a child user)."""
        api_keys = self.all_api_keys()
        my_api_keys = []

        if api_keys["id"] == self.id:
            # This function was called on the authenticated user
            my_api_keys = api_keys["keys"]
        else:
            # This function was called on a child user (authenticated as parent, only return
            # this child user's details).
            for child in api_keys["children"]:
                if child.id == self.id:
                    my_api_keys = child.keys
                    break

        return my_api_keys

    def update_brand(self, api_key: Optional[str] = None, **params) -> "User":
        """Update the User's Brand."""
        requestor = Requestor(local_api_key=api_key)
        response, api_key = requestor.request(
            method=RequestMethod.PATCH, url=self.instance_url() + "/brand", params=params
        )
        return convert_to_easypost_object(response=response, api_key=api_key)
