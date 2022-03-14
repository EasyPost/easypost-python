from easypost.requestor import Requestor
from easypost.resource import AllResource, CreateResource


class Tracker(AllResource, CreateResource):
    @classmethod
    def create_list(cls, trackers, api_key=None):
        requestor = Requestor(api_key)
        url = "%s/%s" % (cls.class_url(), "create_list")
        new_params = {"trackers": trackers}
        _, _ = requestor.request("post", url, new_params)
        return True
