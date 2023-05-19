import re
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.constant import NO_MORE_PAGES_ERROR
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

    def _create_resource(self, class_name: str, **params) -> Any:
        """Create an EasyPost object via the EasyPost API."""
        url = self._class_url(class_name)
        wrapped_params = {self._snakecase_name(class_name): params}

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        return convert_to_easypost_object(response=response)

    def _all_resources(self, class_name: str, **params) -> Any:
        """Retrieve a list of EasyPostObjects from the EasyPost API."""
        url = self._class_url(class_name)

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

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

    def _get_next_page_resources(
        self,
        class_name: str,
        collection: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve next page of EasyPostObjects via the EasyPost API."""
        url = self._class_url(class_name)
        collection_array = collection.get(url[1:])

        if collection_array is None or len(collection_array) == 0 or not collection.get("has_more"):
            raise EndOfPaginationError(NO_MORE_PAGES_ERROR)

        params = {
            "before_id": collection_array[-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        response_array: List[Any] = response.get(url[1:])  # type: ignore
        if response is None or len(response_array) == 0 or not response.get("has_more"):
            raise EndOfPaginationError(NO_MORE_PAGES_ERROR)

        return convert_to_easypost_object(response=response)
