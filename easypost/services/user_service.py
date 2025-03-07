from typing import (
    Any,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import User
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

    def all(self, **params) -> dict[str, Any]:
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

    def update_brand(self, id: str, **params) -> User:
        """Update a User's Brand."""
        url = self._instance_url(self._model_class, id) + "/brand"

        response = Requestor(self._client).request(
            method=RequestMethod.PATCH,
            url=url,
            params=params,
        )

        return convert_to_easypost_object(response=response)

    def all_children(self, **params) -> dict[str, Any]:
        """Retrieve a paginated list of children from the API."""
        url = "/users/children"
        response = Requestor(self._client).request(
            method=RequestMethod.GET,
            url=url,
            params=params,
        )

        return convert_to_easypost_object(response=response)

    def get_next_page_of_children(
        self,
        children: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Retrieve the next page of the list Children response."""
        self._check_has_next_page(collection=children)

        params = {
            "after_id": children["children"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all_children(**params)
