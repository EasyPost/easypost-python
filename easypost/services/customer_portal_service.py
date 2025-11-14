from typing import Any

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class CustomerPortalService(BaseService):
    def __init__(self, client):
        self._client = client

    def create_account_link(self, **params) -> dict[str, Any]:
        """Create a Portal Session."""
        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/customer_portal/account_link",
            params=params,
        )

        return convert_to_easypost_object(response=response)
