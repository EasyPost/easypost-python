from easypost.models.rate import Rate
from easypost.services.base_service import BaseService


class RateService(BaseService):
    def __init__(self, client):
        super().__init__(client=client)

    def retrieve(self, id: str) -> Rate:
        """Retrieve a Rate."""
        return self._retrieve_resource(self._model_class, id)
