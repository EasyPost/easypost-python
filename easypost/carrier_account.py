from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import Requestor
from easypost.resource import (
    AllResource,
    CreateResource,
    DeleteResource,
    UpdateResource,
)


class CarrierAccount(AllResource, CreateResource, UpdateResource, DeleteResource):
    @classmethod
    def types(cls, api_key=None):
        requestor = Requestor(api_key)
        response, api_key = requestor.request("get", "/carrier_types")
        return convert_to_easypost_object(response, api_key)
