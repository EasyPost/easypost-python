from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    AllResource,
    CreateResource,
)


class Tracker(AllResource, CreateResource):
    @classmethod
    def create_list(cls, trackers: List[Dict[str, Any]], api_key: Optional[str] = None) -> bool:
        """Create a list of trackers."""
        requestor = Requestor(local_api_key=api_key)
        url = "%s/%s" % (cls.class_url(), "create_list")
        new_params = {"trackers": trackers}
        _, _ = requestor.request(method=RequestMethod.POST, url=url, params=new_params)
        return True
