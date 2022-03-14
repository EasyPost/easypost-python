from easypost.requestor import Requestor
from easypost.resource import CreateResource


class Pickup(CreateResource):
    def buy(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self

    def cancel(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "cancel")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self
