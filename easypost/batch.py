from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import Requestor
from easypost.resource import AllResource, CreateResource


class Batch(AllResource, CreateResource):
    @classmethod
    def create_and_buy(cls, api_key=None, **params):
        requestor = Requestor(api_key)
        url = "%s/%s" % (cls.class_url(), "create_and_buy")
        wrapped_params = {cls.snakecase_name(): params}
        response, api_key = requestor.request("post", url, wrapped_params)
        return convert_to_easypost_object(response, api_key)

    def buy(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self

    def label(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "label")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self

    def remove_shipments(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "remove_shipments")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self

    def add_shipments(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "add_shipments")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self

    def create_scan_form(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "scan_form")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self
