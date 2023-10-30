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
from easypost.resource import Resource


class User(Resource):
    @classmethod
    def all_children(cls, api_key: Optional[str] = None, **params) -> Dict[str, Any]:
        """Retrieve a paginated list of children from the API."""
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
        children_array = children.get("children", [])

        if len(children_array) == 0 or not children.get("has_more", False):
            raise Error(message="There are no more pages to retrieve.")

        params = {
            "after_id": children_array[-1].id,
            "page_size": page_size,
        }

        data, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params, beta=True)
        next_children_array: List[Any] = data.get("children", [])
        if len(next_children_array) == 0:
            raise Error(message="There are no more pages to retrieve.")

        return convert_to_easypost_object(response=data, api_key=api_key)
