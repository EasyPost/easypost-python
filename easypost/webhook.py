from easypost.requestor import Requestor
from easypost.resource import AllResource, CreateResource, DeleteResource


class Webhook(AllResource, CreateResource, DeleteResource):
    def update(self, **params):
        requestor = Requestor(self._api_key)
        url = self.instance_url()
        response, api_key = requestor.request("put", url, params)
        self.refresh_from(response, api_key)
        return self
