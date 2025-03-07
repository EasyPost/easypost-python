from typing import (
    Any,
)

from easypost.constant import NO_USER_FOUND
from easypost.easypost_object import convert_to_easypost_object
from easypost.errors import FilteringError
from easypost.models import ApiKey
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class ApiKeyService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = ApiKey.__name__

    def all(self) -> dict[str, Any]:
        """Retrieve a list of all API keys."""
        url = "/api_keys"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response)

    def retrieve_api_keys_for_user(self, id: str) -> list[ApiKey]:
        """Retrieve a list of API keys (works for the authenticated User or a child User)."""
        api_keys = self.all()

        if api_keys["id"] == id:
            # This function was called on the authenticated user
            return api_keys["keys"]

        # This function was called on a child user (authenticated as parent, only return
        # this child user's details).
        for child in api_keys["children"]:
            if child.id == id:
                return child.keys

        raise FilteringError(message=NO_USER_FOUND)
