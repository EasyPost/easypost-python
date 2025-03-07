from typing import (
    Any,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.models import Webhook
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class WebhookService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Webhook.__name__

    def create(self, **params) -> Webhook:
        """Create a Webhook."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> dict[str, Any]:
        """Retrieve a list of Webhooks."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id: str) -> Webhook:
        """Retrieve a Webhook."""
        return self._retrieve_resource(self._model_class, id)

    def update(self, id: str, **params) -> Webhook:
        """Update a Webhook."""
        url = self._instance_url(self._model_class, id)

        response = Requestor(self._client).request(method=RequestMethod.PATCH, url=url, params=params)

        return convert_to_easypost_object(response=response)

    def delete(self, id: str) -> None:
        """Delete a Webhook."""
        self._delete_resource(self._model_class, id)
