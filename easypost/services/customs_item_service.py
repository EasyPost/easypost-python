from easypost.models import CustomsItem
from easypost.services.base_service import BaseService


class CustomsItemService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = CustomsItem.__name__

    def create(self, **params) -> CustomsItem:
        """Create a CustomsItem."""
        return self._create_resource(self._model_class, **params)

    def retrieve(self, id: str) -> CustomsItem:
        """Retrieve a CustomsItem."""
        return self._retrieve_resource(self._model_class, id)
