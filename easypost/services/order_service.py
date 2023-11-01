from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Order
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

    def retrieve(self, id: str) -> Order:
        """Retrieve an Order."""
        return self._retrieve_resource(self._model_class, id)

    def get_rates(self, id: str) -> Order:
        """Get rates for an Order."""
        url = f"{self._instance_url(self._model_class, id)}/rates"

        response = Requestor(self._client).request(method=RequestMethod.GET, url=url)

        return convert_to_easypost_object(response=response)

    def buy(self, id: str, **params) -> Order:
        """Buy an Order."""
        url = f"{self._instance_url(self._model_class, id)}/buy"

        response = Requestor(self._client).request(method=RequestMethod.POST, url=url, params=params)

        return convert_to_easypost_object(response=response)
