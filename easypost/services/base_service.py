from typing import (
    Any,
    Dict,
    Optional,
)

from easypost.constant import (
    _FILTERS_KEY,
    NO_MORE_PAGES_ERROR,
)
from easypost.easypost_client import ApiVersion
from easypost.easypost_object import convert_to_easypost_object
from easypost.errors import EndOfPaginationError
from easypost.http import HttpMethod
from easypost.requestor import (
    RequestMethod,
    Requestor,
)


class BaseService:
    """The base service that all other services inherit containing shared logic."""

    def __init__(self, client: "EasyPostClient"):
        self._client: "EasyPostClient" = client

    def request(
        self,
        klass: type,
        method: HttpMethod,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        root_key: Optional[str] = None,
        override_api_version: Optional[ApiVersion] = None,
    ) -> Any:
        """Make a request to the EasyPost API."""
        return self._client.request(
            klass=klass,
            method=method,
            endpoint=endpoint,
            params=params,
            root_key=root_key,
            override_api_version=override_api_version,
        )

    def _create_resource(self, class_name: str, **params) -> Any:
        """Create an EasyPost object via the EasyPost API."""
        url = self._class_url(class_name)
        wrapped_params = {self._snakecase_name(class_name): params}

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def _all_resources(self, class_name: str, filters: Optional[Dict[str, Any]] = None, **params) -> Any:
        """Retrieve a list of EasyPostObjects from the EasyPost API."""
        url = self._class_url(class_name)
        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        if filters:  # presence of filters indicates we are dealing with a paginated response
            response[_FILTERS_KEY] = filters  # Save the filters used to reference in potential get_next_page call

        return convert_to_easypost_object(response=response)

    def _retrieve_resource(self, class_name: str, id: str) -> Any:
        """Retrieve an object from the EasyPost API."""
        url = self._instance_url(class_name, id)

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response)

    def _update_resource(self, class_name: str, id: str, method: RequestMethod = RequestMethod.PATCH, **params) -> Any:
        """Update an EasyPost object via the EasyPost API."""
        url = self._instance_url(class_name, id)
        wrapped_params = {self._snakecase_name(class_name): params}

        response = Requestor(self._client).request(method=method, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def _delete_resource(self, class_name: str, id: str) -> Any:
        """Delete an EasyPost object via the EasyPost API."""
        url = self._instance_url(class_name, id)

        response = Requestor(self._client).request(method=RequestMethod.DELETE, url=url)

        return convert_to_easypost_object(response=response)

    def _check_has_next_page(self, collection: Dict[str, Any]) -> None:
        """Raise exception if there is no next page of a collection."""
        if not collection.get("has_more", False):
            raise EndOfPaginationError(NO_MORE_PAGES_ERROR)
