from typing import (
    Any,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import (
    Shipment,
)
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class LumaService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = "Luma"

    def get_promises(
        self,
        **params: dict[str, Any],
    ) -> Shipment:
        """Get Luma promises on what rates meet your criteria."""
        url = "/luma/promise"
        wrapped_params = {
            self._snakecase_name("Shipment"): params,
        }

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)
