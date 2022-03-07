import easypost.easypost_object as util
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
        return util.convert_to_easypost_object(response, api_key)
