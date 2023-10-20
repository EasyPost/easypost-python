from typing import (
    Any,
    Optional,
    List, Dict,
)

from easypost.error import Error
from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import Resource


class User(Resource):
    @classmethod
    def retrieve_all_children(cls, api_key: Optional[str] = None, **params) -> Dict[str, Any]:
        """Retrieve a list of children from the API."""
        requestor = Requestor(local_api_key=api_key)
        url = "/users/children"
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params, beta=True)
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def get_next_page_of_children(
            cls,
            children: Dict[str, Any],
            page_size: int,
            api_key: Optional[str] = None,
    ) -> List["User"]:
        """Get next page of children."""
        requestor = Requestor(local_api_key=api_key)
        url = "/users/children"
        children_array = children.get('children', [])

        if children_array is None or len(children_array) == 0 or not children.get("has_more"):
            raise Error(message="There are no more pages to retrieve.")

        params = {
            "after_id": children_array[-1].id,
            "page_size": page_size,
        }

        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params, beta=True)
        response_array: List[Any] = response.get(url[1:])  # type: ignore
        if response is None or len(response_array) == 0 or not response.get("has_more"):
            raise Error(message="There are no more pages to retrieve.")

        return convert_to_easypost_object(response=response, api_key=api_key)
