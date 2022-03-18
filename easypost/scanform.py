from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import Requestor
from easypost.resource import AllResource, CreateResource


class ScanForm(AllResource, CreateResource):
    @classmethod
    def create(cls, api_key=None, **params):
        requestor = Requestor(api_key)
        url = cls.class_url()
        response, api_key = requestor.request("post", url, params)
        return convert_to_easypost_object(response, api_key)
