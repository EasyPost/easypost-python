from typing import (
    Any,
    List,
    Optional,
)

from easypost.constant import _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS
from easypost.easypost_object import convert_to_easypost_object
from easypost.models import CarrierAccount
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class CarrierAccountService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = CarrierAccount.__name__

    def create(self, **params) -> CarrierAccount:
        """Creates a CarrierAccount."""
        carrier_account_type = params.get("type")

        if carrier_account_type is None:
            raise ValueError("Missing required parameter 'type'")

        url = self._select_carrier_account_creation_endpoint(carrier_account_type=carrier_account_type)
        wrapped_params = {self._snakecase_name(self._model_class): params}
        response, api_key = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response, api_key=api_key)

    def all(self, **params) -> List[Any]:
        """Retrieve a list of CarrierAccounts."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id) -> CarrierAccount:
        """Retrieve a CarrierAccount."""
        return self._retrieve_resource(self._model_class, id)

    def update(self, id, **params) -> CarrierAccount:
        """Update a CarrierAccount."""
        return self._update_resource(self._model_class, id, **params)

    def delete(self, id):
        """Delete a CarrierAccount."""
        self._delete_resource(self._model_class, id)

    def types(self) -> List[str]:
        """Get the types of CarrierAccounts available to the User."""
        response, api_key = Requestor(self._client).request(method=RequestMethod.GET, url="/carrier_types")

        return convert_to_easypost_object(response=response, api_key=api_key)

    def _select_carrier_account_creation_endpoint(self, carrier_account_type: Optional[Any]) -> str:
        """Determines which API endpoint to use for the creation call."""
        if carrier_account_type in _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS:
            return "/carrier_accounts/register"

        return "/carrier_accounts"
