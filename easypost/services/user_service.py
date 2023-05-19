from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import (
    ApiKey,
    User,
)
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = User.__name__

    def create(self, **params) -> User:
        """Create a User."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of Users."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id: Optional[str] = None) -> User:
        """Retrieve a User.

        If no id is passed, retrieve the authenticated User.
        """
        if id:
            url = self._instance_url(self._model_class, id)
        else:
            url = self._class_url(self._model_class)

        response = Requestor(self._client).request(
            method=RequestMethod.GET,
            url=url,
        )

        return convert_to_easypost_object(response=response)

    def update(self, id: str, **params) -> User:
        """Update a User."""
        return self._update_resource(self._model_class, id, **params)

    def delete(self, id: str) -> None:
        """Delete a User."""
        self._delete_resource(self._model_class, id)

    def retrieve_me(self) -> User:
        """Retrieve the authenticated User."""
        url = self._class_url(self._model_class)

        response = Requestor(self._client).request(
            method=RequestMethod.GET,
            url=url,
        )

        return convert_to_easypost_object(response=response)

    def all_api_keys(self) -> Dict[str, Any]:
        """Retrieve a list of all API keys."""
        url = "/api_keys"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response)

    def api_keys(self, id: str) -> List[ApiKey]:
        """Retrieve a list of API keys (works for the authenticated User or a child User)."""
        api_keys = self.all_api_keys()
        my_api_keys = []

        if api_keys["id"] == id:
            # This function was called on the authenticated user
            my_api_keys = api_keys["keys"]
        else:
            # This function was called on a child user (authenticated as parent, only return
            # this child user's details).
            for child in api_keys["children"]:
                if child.id == id:
                    my_api_keys = child.keys
                    break

        return my_api_keys

    def update_brand(self, id: str, **params) -> User:
        """Update a User's Brand."""
        url = self._instance_url(self._model_class, id) + "/brand"

        response = Requestor(self._client).request(
            method=RequestMethod.PATCH,
            url=url,
            params=params,
        )

        return convert_to_easypost_object(response=response)
