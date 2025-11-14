from typing import Any

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class EmbeddableService(BaseService):
    def __init__(self, client):
        self._client = client

    def create_session(self, **params) -> dict[str, Any]:
        """Create an Embeddables Session."""
        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/embeddables/session",
            params=params,
        )

        return convert_to_easypost_object(response=response)
