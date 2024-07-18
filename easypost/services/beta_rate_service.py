from typing import (
    Any,
    Dict,
)

from easypost.easypost_client import ApiVersion
from easypost.easypost_object import convert_to_easypost_object
from easypost.http import HttpMethod
from easypost.models.rate import Rate
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class BetaRateService(BaseService):
    def __init__(self, client):
        super().__init__(client=client)

    def retrieve_stateless_rates(self, **params) -> Dict[str, Any]:
        """Retrieves stateless rates by passing shipment data."""
        endpoint = f"rates"
        method = HttpMethod.POST

        wrapped_params = {"shipment": params}

        return self.request(
            klass=Rate,
            method=method,
            endpoint=endpoint,
            params=params,
            root_key="rates",
            override_api_version=ApiVersion.Beta,
        )

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url=url,
            params=wrapped_params,
            beta=True,
        )

        return convert_to_easypost_object(response=response.get("rates", None))
