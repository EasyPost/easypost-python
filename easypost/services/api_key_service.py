from typing import (
    Any,
    Dict,
    List,
)

from easypost.constant import NO_USER_FOUND
from easypost.easypost_object import convert_to_easypost_object
from easypost.errors import FilteringError
from easypost.http import HttpMethod
from easypost.models.api_key import ApiKey
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class ApiKeyService(BaseService):
    def __init__(self, client):
        super().__init__(client=client)

    def all(self) -> Dict[str, Any]:
        """Retrieve a list of all API keys."""
        endpoint = "api_keys"
        method = HttpMethod.GET

        return self.request(klass=ApiKey, method=method, endpoint=endpoint)

    def retrieve_api_keys_for_user(self, id: str) -> List[ApiKey]:
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
