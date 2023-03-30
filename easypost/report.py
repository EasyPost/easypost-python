from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import Resource


class Report(Resource):
    @classmethod
    def create(cls, api_key: Optional[str] = None, **params) -> "Report":
        """Create a report."""
        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{params.get('type')}"
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def all(cls, api_key: Optional[str] = None, **params) -> List["Report"]:
        """Retrieve all reports."""
        requestor = Requestor(local_api_key=api_key)
        type = params.pop("type")
        url = f"{cls.class_url()}/{type}"
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)
        response["type"] = type
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def get_next_page(
        cls,
        reports: Dict[str, Any],
        page_size: int = None,
        api_key: Optional[str] = None,
    ) -> List["Report"]:
        """Get next page of Report collection"""
        requestor = Requestor(local_api_key=api_key)
        type = reports.get("type")
        url = f"{cls.class_url()}/{type}"
        params = {
            "before_id": reports["reports"][-1].id,
            "page_size": page_size,
        }
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)
        return convert_to_easypost_object(response=response, api_key=api_key)
