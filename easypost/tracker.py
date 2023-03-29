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
from easypost.resource import (
    AllResource,
    CreateResource,
    NextPageResource,
)


class Tracker(AllResource, CreateResource, NextPageResource):
    @classmethod
    def create_list(cls, trackers: List[Dict[str, Any]], api_key: Optional[str] = None) -> bool:
        """Create a list of trackers."""
        requestor = Requestor(local_api_key=api_key)
        url = "%s/%s" % (cls.class_url(), "create_list")
        new_params = {"trackers": trackers}
        _, _ = requestor.request(method=RequestMethod.POST, url=url, params=new_params)
        return True

    @classmethod
    def all(cls, api_key: Optional[str] = None, **params) -> List["Tracker"]:
        """Retrieve a list of Trackers."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)
        response["tracking_code"] = params.get("tracking_code")
        response["carrier"] = params.get("carrier")
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def get_next_page(
        cls,
        trackers: Dict[str, Any],
        page_size: int,
        api_key: Optional[str] = None,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> List["Tracker"]:
        """Get next page of Tracker collection."""
        optional_params = {
            "tracking_code": trackers.get("tracking_code"),
            "carrier": trackers.get("carrier"),
        }
        return super().get_next_page(trackers, page_size, api_key, optional_params)
