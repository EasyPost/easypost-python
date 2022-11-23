from typing import (
    Any,
    List,
    Optional,
)

from easypost.constant import _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS
from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    AllResource,
    CreateResource,
    DeleteResource,
    UpdateResource,
)


def _select_carrier_account_creation_endpoint(carrier_account_type: Optional[Any]) -> str:
    """Determines which API endpoint to use for the creation call."""
    if carrier_account_type in _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS:
        return "/carrier_accounts/register"

    return "/carrier_accounts"


class CarrierAccount(AllResource, CreateResource, UpdateResource, DeleteResource):
    @classmethod
    def types(cls, api_key: Optional[str] = None) -> List[str]:
        """Get the types of carrier accounts available to the user."""
        requestor = Requestor(local_api_key=api_key)
        response, api_key = requestor.request(method=RequestMethod.GET, url="/carrier_types")
        return convert_to_easypost_object(response=response, api_key=api_key)

    # Overrides CreateResource.create
    @classmethod
    def create(cls, api_key: Optional[str] = None, **params) -> "CarrierAccount":
        """Creates a Carrier Account that requires custom registration (eg: FedEx & UPS)."""
        requestor = Requestor(local_api_key=api_key)

        carrier_account_type = params.get("type")

        if carrier_account_type is None:
            raise ValueError("Missing required parameter 'type'")

        url = _select_carrier_account_creation_endpoint(carrier_account_type=carrier_account_type)
        wrapped_params = {cls.snakecase_name(): params}
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        return convert_to_easypost_object(response=response, api_key=api_key)
