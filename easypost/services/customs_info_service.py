from easypost.models.customs_info import CustomsInfo
from easypost.services.base_service import BaseService


class CustomsInfoService(BaseService):
    def __init__(self, client):
        super().__init__(client=client)

    def create(self, **params) -> CustomsInfo:
        """Create a CustomsInfo."""
        return self._create_resource(self._model_class, **params)

    def retrieve(self, id: str) -> CustomsInfo:
        """Retrieve a CustomsInfo."""
        return self._retrieve_resource(self._model_class, id)
