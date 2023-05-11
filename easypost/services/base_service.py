import re
from enum import Enum
from typing import (
    Any,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)


class BaseService:
    """The base service that all other services inherit."""

    def __init__(self, client):
        self.client = client

    def snakecase_name() -> str:
        """Return the class name as snake_case."""
        snake_name = (cls.__name__[0:1] + re.sub(r"([A-Z])", r"_\1", cls.__name__[1:])).lower()
        return snake_name

    def class_url(self, class_name) -> str:
        """Generate a URL based on class name."""
        if class_name[-1:] in ("s", "h"):
            return "/%ses" % class_name
        else:
            return "/%ss" % class_name

    # def instance_url(self) -> str:
    #     """Generate an instance URL based on the ID of the object."""
    #     easypost_id = self.get("id")
    #     if not easypost_id:
    #         raise Error("%s instance has invalid ID: %r" % (type(self).__name__, easypost_id))
    #     return "%s/%s" % (self.class_url(), easypost_id)

    def all_resources(self, class_name, **params) -> List[Any]:
        """Retrieve a list of records from the API."""
        requestor = Requestor()
        url = self.class_url(class_name)
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)

        return convert_to_easypost_object(response=response, api_key=api_key)
