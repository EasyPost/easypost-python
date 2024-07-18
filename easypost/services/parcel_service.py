from easypost.models.parcel import Parcel
from easypost.services.base_service import BaseService


class ParcelService(BaseService):
    def __init__(self, client):
        super().__init__(client=client)

    def create(self, **params) -> Parcel:
        """Create a Parcel."""
        return self._create_resource(self._model_class, **params)

    def retrieve(self, id: str) -> Parcel:
        """Retrieve a Parcel."""
        return self._retrieve_resource(self._model_class, id)
