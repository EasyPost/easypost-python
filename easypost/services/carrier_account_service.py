from typing import (
    Any,
    Optional,
)

from easypost.constant import (
    _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_OAUTH,
    _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS,
    MISSING_PARAMETER_ERROR,
)
from easypost.easypost_object import convert_to_easypost_object
from easypost.errors import MissingParameterError
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
        """Create a CarrierAccount."""
        carrier_account_type = params.get("type")

        if carrier_account_type is None:
            raise MissingParameterError(MISSING_PARAMETER_ERROR.format("type"))

        url = self._select_carrier_account_creation_endpoint(carrier_account_type=carrier_account_type)
        if carrier_account_type in _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_OAUTH:
            wrapped_params = {"carrier_account_oauth_registrations": params}
        else:
            wrapped_params = {self._snakecase_name(self._model_class): params}

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of CarrierAccounts."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id: str) -> CarrierAccount:
        """Retrieve a CarrierAccount."""
        return self._retrieve_resource(self._model_class, id)

    def update(self, id: str, **params) -> CarrierAccount:
        """Update a CarrierAccount."""
        return self._update_resource(self._model_class, id, **params)

    def delete(self, id: str) -> None:
        """Delete a CarrierAccount."""
        self._delete_resource(self._model_class, id)

    def types(self) -> list[dict[str, Any]]:
        """Get the types of CarrierAccounts available to the User."""
        response = Requestor(self._client).request(method=RequestMethod.GET, url="/carrier_types")

        return convert_to_easypost_object(response=response)

    def _select_carrier_account_creation_endpoint(self, carrier_account_type: Optional[Any]) -> str:
        """Determines which API endpoint to use for the creation call."""
        if carrier_account_type in _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS:
            return "/carrier_accounts/register"
        elif carrier_account_type in _CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_OAUTH:
            return "/carrier_accounts/register_oauth"

        return "/carrier_accounts"
