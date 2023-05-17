from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Report
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class ReportService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Report.__name__

    def create(self, **params) -> Report:
        """Create a Report."""
        url = f"{self._class_url(self._model_class)}/{params.pop('type')}"

        response, api_key = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> List[Report]:
        """Retrieve a list of all Reports."""
        type = params.pop("type")
        url = f"{self._class_url(self._model_class)}/{type}"

        response, api_key = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)
        response["type"] = type  # Needed for retrieving the next page

        return convert_to_easypost_object(response=response)

    def retrieve(self, id) -> Report:
        """Retrieve a Report."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        reports: Dict[str, Any],
        page_size: Optional[int] = None,
        api_key: Optional[str] = None,
    ) -> List[Report]:
        """Retrieve the next page of the list Report response."""
        type = reports.get("type")
        url = f"{self._class_url(self._model_class)}/{type}"
        params = {
            "before_id": reports["reports"][-1].id,
            "page_size": page_size,
        }

        response, api_key = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        return convert_to_easypost_object(response=response)
