from easypost.requestor import Requestor
from easypost.resource import CreateResource


class Order(CreateResource):
    def get_rates(self):
        """Get rates for an order."""
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "rates")
        response, api_key = requestor.request("get", url)
        self.refresh_from(response, api_key)
        return self

    def buy(self, **params):
        """Buy an order."""
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self
