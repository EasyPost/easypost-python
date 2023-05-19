from typing import (
    Any,
    Dict,
    Optional,
)

from easypost.constant import MISSING_PARAMETER_ERROR
from easypost.easypost_object import convert_to_easypost_object
from easypost.errors import MissingParameterError
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
        refund_type = params.pop("type")

        if refund_type is None:
            raise MissingParameterError(MISSING_PARAMETER_ERROR.format("type"))

        url = f"{self._class_url(self._model_class)}/{refund_type}"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of Reports."""
        refund_type = params.pop("type")

        if refund_type is None:
            raise MissingParameterError(MISSING_PARAMETER_ERROR.format("type"))

        url = f"{self._class_url(self._model_class)}/{refund_type}"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)
        response["type"] = refund_type  # Needed for retrieving the next page

        return convert_to_easypost_object(response=response)

    def retrieve(self, id: str) -> Report:
        """Retrieve a Report."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        reports: Dict[str, Any],
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve the next page of the list Report response."""
        refund_type = reports.get("type")

        if refund_type is None:
            raise MissingParameterError(MISSING_PARAMETER_ERROR.format("type"))

        url = f"{self._class_url(self._model_class)}/{refund_type}"
        params = {
            "before_id": reports["reports"][-1].id,
            "page_size": page_size,
        }

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        return convert_to_easypost_object(response=response)
