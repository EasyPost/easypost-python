from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models.order import Order
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class OrderService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Order.__name__

    def create(self, **params) -> Order:
        """Create an Order."""
        return self._create_resource(self._model_class, **params)

    def retrieve(self, id) -> Order:
        """Retrieve an Order."""
        return self._retrieve_resource(self._model_class, id)

    def get_next_page(
        self,
        insurances: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> List[Order]:
        """Retrieve the next page of the list Order response."""
        return self._get_next_page_resources(self._model_class, insurances, page_size, optional_params)

    def get_rates(self, id: str) -> Order:
        """Get rates for an Order."""
        url = f"{self._instance_url(self._model_class, id)}/rates"

        response, api_key = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response, api_key=api_key)

    def buy(self, id: str, **params) -> Order:
        """Buy an Order."""
        url = f"{self._instance_url(self._model_class, id)}/buy"

        response, api_key = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response, api_key=api_key)
