import re
from typing import (
    Any,
    Optional,
)

from easypost.constant import (
    _FILTERS_KEY,
    NO_MORE_PAGES_ERROR,
)
from easypost.easypost_object import convert_to_easypost_object
from easypost.errors import EndOfPaginationError
from easypost.requestor import (
    RequestMethod,
    Requestor,
)


class BaseService:
    """The base service that all other services inherit containing shared logic."""

    def __init__(self, client):
        self._client = client

    def _snakecase_name(self, class_name: str) -> str:
        """Return the class name as snake_case."""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()

    def _class_url(self, class_name: str) -> str:
        """Generate a URL based on class name."""
        transformed_class_name = self._snakecase_name(class_name)
        if transformed_class_name[-1:] in ("s", "h"):
            return f"/{transformed_class_name}es"
        else:
            return f"/{transformed_class_name}s"

    def _instance_url(self, class_name: str, id: str) -> str:
        """Generate an instance URL based on a class name and ID."""
        return f"{self._class_url(class_name)}/{id}"

    def _create_resource(self, class_name: str, beta: bool = False, **params) -> Any:
        """Create an EasyPost object via the EasyPost API."""
        url = self._class_url(class_name)
        wrapped_params = {self._snakecase_name(class_name): params}

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params, beta=beta)

        return convert_to_easypost_object(response=response)

    def _all_resources(
        self,
        class_name: str,
        filters: Optional[dict[str, Any]] = None,
        beta: bool = False,
        **params,
    ) -> Any:
        """Retrieve a list of EasyPostObjects from the EasyPost API."""
        url = self._class_url(class_name)
        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params, beta=beta)

        if filters:  # presence of filters indicates we are dealing with a paginated response
            response[_FILTERS_KEY] = filters  # Save the filters used to reference in potential get_next_page call

        return convert_to_easypost_object(response=response)

    def _retrieve_resource(self, class_name: str, id: str, beta: bool = False) -> Any:
        """Retrieve an object from the EasyPost API."""
        url = self._instance_url(class_name, id)

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, beta=beta)

        return convert_to_easypost_object(response=response)

    def _update_resource(
        self,
        class_name: str,
        id: str,
        method: RequestMethod = RequestMethod.PATCH,
        beta: bool = False,
        **params,
    ) -> Any:
        """Update an EasyPost object via the EasyPost API."""
        url = self._instance_url(class_name, id)
        wrapped_params = {self._snakecase_name(class_name): params}

        response = Requestor(self._client).request(method=method, url=url, params=wrapped_params, beta=beta)

        return convert_to_easypost_object(response=response)

    def _delete_resource(self, class_name: str, id: str, beta: bool = False) -> Any:
        """Delete an EasyPost object via the EasyPost API."""
        url = self._instance_url(class_name, id)

        response = Requestor(self._client).request(method=RequestMethod.DELETE, url=url, beta=beta)

        return convert_to_easypost_object(response=response)

    def _check_has_next_page(self, collection: dict[str, Any]) -> None:
        """Raise exception if there is no next page of a collection."""
        if not collection.get("has_more", False):
            raise EndOfPaginationError(NO_MORE_PAGES_ERROR)
