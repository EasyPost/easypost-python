from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class CarrierMetadataService(BaseService):
    def __init__(self, client):
        self._client = client

    def retrieve(
        self,
        carriers: Optional[List[str]] = None,
        types: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get metadata for all carriers on the EasyPost platform or specify optional filters."""
        params = {
            "carriers": ",".join(carriers) if carriers else None,
            "types": ",".join(types) if types else None,
        }

        response = Requestor(self._client).request(
            method=RequestMethod.GET,
            url="/metadata/carriers",
            params=params,
        )

        return convert_to_easypost_object(response=response.get("carriers", []))
