from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from warnings import warn

from easypost.constant import _FILTERS_KEY
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
        filters = {
            "key": "trackers",
            "tracking_code": params.get("tracking_code"),
            "carrier": params.get("carrier"),
        }

        return self._all_resources(self._model_class, filters, **params)

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
        self._check_has_next_page(collection=trackers)

        params = {
            "before_id": trackers["trackers"][-1].id,
            "page_size": page_size,
            "tracking_code": trackers.get(_FILTERS_KEY, {}).get(
                "tracking_code"
            ),  # Use the same tracking_code as the last page
            "carrier": trackers.get(_FILTERS_KEY, {}).get("carrier"),  # Use the same carrier as the last page
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)

    def create_list(self, trackers: List[Dict[str, Any]]) -> None:
        """Create a list of Trackers.

        NOTE: This function is deprecated, use the create function instead.
        """
        warn(
            "This function is deprecated, use the create function instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        url = f"{self._class_url(self._model_class)}/create_list"
        wrapped_params = {"trackers": trackers}

        Requestor(self._client).request(method=RequestMethod.POST, url=url, params=wrapped_params)
