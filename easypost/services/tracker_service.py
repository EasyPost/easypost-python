from typing import (
    Any,
    Optional,
)

from easypost.constant import _FILTERS_KEY
from easypost.models import Tracker
from easypost.services.base_service import BaseService


class TrackerService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Tracker.__name__

    def create(self, **params) -> Tracker:
        """Create a Tracker."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Trackers."""
        filters = {
            "key": "trackers",
            "tracking_code": params.get("tracking_code"),
            "tracking_codes": params.get("tracking_codes"),
            "carrier": params.get("carrier"),
        }
        # Make Ruby on Rails happy with proper URL encoding
        if params.get("tracking_codes"):
            params["tracking_codes[]"] = params.pop("tracking_codes")

        return self._all_resources(self._model_class, filters, **params)

    def retrieve(self, id: str) -> Tracker:
        """Retrieve a Tracker."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        trackers: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
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
