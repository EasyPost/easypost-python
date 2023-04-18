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


class CarrierMetadata:
    @classmethod
    def retrieve_carrier_metadata(
        cls, api_key: Optional[str] = None, carriers: Optional[List[str]] = None, types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get carrier metadata for all carriers on the EasyPost platform."""
        requestor = Requestor(local_api_key=api_key)
        params = {
            "carriers": ",".join(carriers) if carriers else None,
            "types": ",".join(types) if types else None,
        }
        response, api_key = requestor.request(method=RequestMethod.GET, url="/metadata", params=params, beta=True)
        return convert_to_easypost_object(response=response.get("carriers", []), api_key=api_key)
