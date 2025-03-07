from typing import (
    Any,
    Optional,
)

from easypost.constant import (
    _FILTERS_KEY,
    MISSING_PARAMETER_ERROR,
)
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
        report_type = params.pop("type")

        if report_type is None:
            raise MissingParameterError(MISSING_PARAMETER_ERROR.format("type"))

        url = f"{self._class_url(self._model_class)}/{report_type}"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Reports."""
        # Capture some of the parameters used for later reference
        filters = {
            "key": "reports",
            "type": params.get("type", None),
        }

        report_type = params.pop("type")
        if report_type is None:
            raise MissingParameterError(MISSING_PARAMETER_ERROR.format("type"))

        url = f"{self._class_url(self._model_class)}/{report_type}"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url, params=params)

        response[_FILTERS_KEY] = filters  # Save the filters used to reference in potential get_next_page call

        return convert_to_easypost_object(response=response)

    def retrieve(self, id: str) -> Report:
        """Retrieve a Report."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        reports: dict[str, Any],
        page_size: Optional[int] = None,
        optional_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Retrieve the next page of the list Report response."""
        self._check_has_next_page(collection=reports)

        params = {
            "before_id": reports["reports"][-1].id,
            "page_size": page_size,
            "type": reports.get(_FILTERS_KEY, {}).get("type"),  # Use the same type as the last page
        }

        if optional_params:
            params.update(optional_params)

        return self.all(**params)
