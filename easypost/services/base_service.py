import re
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.error import Error
from easypost.requestor import (
    RequestMethod,
    Requestor,
)


class BaseService:
    """The base service that all other services inherit."""

    def __init__(self, client):
        self._client = client

    def _snakecase_name(self, class_name) -> str:
        """Return the class name as snake_case."""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()

    def _class_url(self, class_name) -> str:
        """Generate a URL based on class name."""
        transformed_class_name = self._snakecase_name(class_name)
        if transformed_class_name[-1:] in ("s", "h"):
            return f"/{transformed_class_name}es"
        else:
            return f"/{transformed_class_name}s"

    def _instance_url(self, class_name, id) -> str:
        """Generate an instance URL based on the ID of the object."""
        if not id:
            raise Error(f"{class_name} instance has invalid ID: {id}")

        _class_url = self._class_url(class_name)

        return f"{_class_url}/{id}"

    def _create_resource(self, class_name: str, **params) -> Any:
        """Create an EasyPost object."""
        url = self._class_url(class_name)
        wrapped_params = {self._snakecase_name(class_name): params}

        # TODO: Don't instantiate the Requestor class, pass the client directly to the request
        response, api_key = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)

        # TODO: Get rid of the api_key
        return convert_to_easypost_object(response=response, api_key=api_key)

    def _all_resources(self, class_name: str, **params) -> List[Any]:
        """Retrieve a list of records from the EasyPost API."""
        url = self._class_url(class_name)
        # TODO: Don't instantiate the Requestor class, pass the client directly to the request
        response, api_key = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        # TODO: Get rid of the api_key
        return convert_to_easypost_object(response=response, api_key=api_key)

    def _retrieve_resource(self, class_name: str, id: str) -> Any:
        """Retrieve an object from the EasyPost API."""
        url = self._instance_url(class_name, id)
        # TODO: Don't instantiate the Requestor class, pass the client directly to the request
        response, api_key = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        # TODO: Get rid of the api_key
        return convert_to_easypost_object(response=response, api_key=api_key)

    def _update_resource(self, class_name: str, id: str, method: RequestMethod = RequestMethod.PATCH, **params) -> Any:
        """Update an EasyPost object."""
        url = self._instance_url(class_name, id)
        wrapped_params = {self._snakecase_name(class_name): params}

        # TODO: Don't instantiate the Requestor class, pass the client directly to the request
        response, api_key = Requestor(self._client).request(method=method, url=url, params=wrapped_params)

        # TODO: Get rid of the api_key
        return convert_to_easypost_object(response=response, api_key=api_key)

    def _delete_resource(self, class_name: str, id: str) -> Any:
        """Delete an EasyPost object."""
        url = self._instance_url(class_name, id)
        # TODO: Don't instantiate the Requestor class, pass the client directly to the request
        response, api_key = Requestor(self._client).request(method=RequestMethod.DELETE, url=url)

        # TODO: Get rid of the api_key
        return convert_to_easypost_object(response=response, api_key=api_key)

    def _get_next_page_resources(
        self,
        class_name: str,
        collection: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Retrieve next page of a specific collection."""
        url = self._class_url(class_name)
        collection_array = collection.get(url[1:])

        if collection_array is None or len(collection_array) == 0 or not collection.get("has_more"):
            raise Error(message="There are no more pages to retrieve.")

        params = {
            "before_id": collection_array[-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        # TODO: Don't instantiate the Requestor class, pass the client directly to the request
        response, api_key = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        response_array: List[Any] = response.get(url[1:])  # type: ignore
        if response is None or len(response_array) == 0 or not response.get("has_more"):
            raise Error(message="There are no more pages to retrieve.")

        return convert_to_easypost_object(response=response, api_key=api_key)
