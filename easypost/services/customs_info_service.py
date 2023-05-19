from easypost.models import CustomsInfo
from easypost.services.base_service import BaseService


class CustomsInfoService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = CustomsInfo.__name__

    def create(self, **params) -> CustomsInfo:
        """Create a CustomsInfo."""
        return self._create_resource(self._model_class, **params)

    def retrieve(self, id: str) -> CustomsInfo:
        """Retrieve a CustomsInfo."""
        return self._retrieve_resource(self._model_class, id)
