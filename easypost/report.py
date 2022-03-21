from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import Requestor
from easypost.resource import AllResource, CreateResource


class Report(AllResource, CreateResource):
    @classmethod
    def create(cls, api_key=None, **params):
        """Create a report."""
        requestor = Requestor(api_key)
        url = "%s/%s" % (cls.class_url(), params["type"])
        response, api_key = requestor.request("post", url, params, False)
        return convert_to_easypost_object(response, api_key)

    @classmethod
    def all(cls, api_key=None, **params):
        """Retrieve all reports."""
        requestor = Requestor(api_key)
        url = "%s/%s" % (cls.class_url(), params["type"])
        response, api_key = requestor.request("get", url, params)
        return convert_to_easypost_object(response, api_key)
