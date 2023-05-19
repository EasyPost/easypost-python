from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Tracker
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class TrackerService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Tracker.__name__

    def create(self, **params) -> Tracker:
        """Create a Tracker."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of Trackers."""
        url = self._class_url(self._model_class)

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)
        response["tracking_code"] = params.get("tracking_code")
        response["carrier"] = params.get("carrier")

        return convert_to_easypost_object(response=response)

    def retrieve(self, id: str) -> Tracker:
        """Retrieve a Tracker."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        trackers: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve the next page of the list Tracker response."""
        optional_params = {
            "tracking_code": trackers.get("tracking_code"),
            "carrier": trackers.get("carrier"),
        }

        return self._get_next_page_resources(self._model_class, trackers, page_size, optional_params)

    def create_list(self, trackers: List[Dict[str, Any]]) -> None:
        """Create a list of Trackers."""
        url = f"{self._class_url(self._model_class)}/create_list"
        wrapped_params = {"trackers": trackers}

        Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)
