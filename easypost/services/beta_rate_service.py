from typing import (
    Any,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Rate
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class BetaRateService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Rate.__name__

    def retrieve_stateless_rates(self, **params) -> dict[str, Any]:
        """Retrieves stateless rates by passing shipment data."""
        url = self._class_url(self._model_class)
        wrapped_params = {"shipment": params}

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url=url,
            params=wrapped_params,
            beta=True,
        )

        return convert_to_easypost_object(response=response.get("rates", None))
