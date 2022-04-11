from typing import Optional

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import Requestor
from easypost.resource import (
    AllResource,
    CreateResource,
)


class Report(AllResource, CreateResource):
    @classmethod
    def create(cls, api_key: Optional[str] = None, **params):
        """Create a report."""
        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{params.get('type')}"
        response, api_key = requestor.request(method="post", url=url, params=params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def all(cls, api_key: Optional[str] = None, **params):
        """Retrieve all reports."""
        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{params.get('type')}"
        response, api_key = requestor.request(method="get", url=url, params=params)
        return convert_to_easypost_object(response=response, api_key=api_key)
