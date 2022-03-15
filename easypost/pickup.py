from easypost.requestor import Requestor
from easypost.resource import CreateResource


class Pickup(CreateResource):
    def buy(self, **params) -> "Pickup":
        """Buy a pickup."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request(method="post", url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def cancel(self, **params) -> "Pickup":
        """Cancel a pickup."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "cancel")
        response, api_key = requestor.request(method="post", url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self
