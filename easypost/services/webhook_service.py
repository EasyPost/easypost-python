from typing import (
    Any,
    Dict,
)

from easypost.models.webhook import Webhook
from easypost.services.base_service import BaseService


class WebhookService(BaseService):
    def __init__(self, client):
        super().__init__(client=client)

    def create(self, **params) -> Webhook:
        """Create a Webhook."""
        return self._create_resource(self._model_class, **params)

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of Webhooks."""
        return self._all_resources(self._model_class, **params)

    def retrieve(self, id: str) -> Webhook:
        """Retrieve a Webhook."""
        return self._retrieve_resource(self._model_class, id)

    def update(self, id: str, **params) -> Webhook:
        """Update a Webhook."""
        return self._update_resource(self._model_class, id, **params)

    def delete(self, id: str) -> None:
        """Delete a Webhook."""
        self._delete_resource(self._model_class, id)
