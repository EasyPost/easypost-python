from easypost.models import Rate
from easypost.services.base_service import BaseService


class RateService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = Rate.__name__

    def retrieve(self, id: str) -> Rate:
        """Retrieve a Rate."""
        return self._retrieve_resource(self._model_class, id)
