from typing import (
    Any,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import (
    Event,
    Payload,
)
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class EventService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Event.__name__

    def create(self, **params) -> Event:
        """Create an Event."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Events."""
        filters = {
            "key": "events",
        }

        return self._all_resources(self._model_class, filters, **params)

    def retrieve(self, id: str) -> Event:
        """Retrieve an Event."""
        return self._retrieve_resource(self._model_class, id)

    def retrieve_all_payloads(self, event_id: str, **params) -> dict[str, Any]:
        """Retrieve a list of Payloads for an Event."""
        url = f"{self._class_url(self._model_class)}/{event_id}/payloads"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def retrieve_payload(self, event_id: str, payload_id: str, **params) -> Payload:
        """Retrieve a Payload of an Event."""
        url = f"{self._class_url(self._model_class)}/{event_id}/payloads/{payload_id}"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def get_next_page(
        self,
        events: dict[str, Any],
        page_size: int,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Retrieve the next page of the list Events response."""
        self._check_has_next_page(collection=events)

        params = {
            "before_id": events["events"][-1].id,
            "page_size": page_size,
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)
