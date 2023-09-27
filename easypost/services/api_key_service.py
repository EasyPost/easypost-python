from typing import (
    Any,
    Dict,
    List,
)

from easypost.easypost_object import convert_to_easypost_object
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

    def all(self) -> Dict[str, Any]:
        """Retrieve a list of all API keys."""
        url = "/api_keys"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response)

    def retrieve_api_keys_for(self, id: str) -> List[ApiKey]:
        """Retrieve a list of API keys (works for the authenticated User or a child User)."""
        api_keys = self.all()
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
