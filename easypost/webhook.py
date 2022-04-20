from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    AllResource,
    CreateResource,
    DeleteResource,
)


class Webhook(AllResource, CreateResource, DeleteResource):
    def update(self, **params) -> "Webhook":
        """Update a webhook."""
        requestor = Requestor(local_api_key=self._api_key)
        url = self.instance_url()
        response, api_key = requestor.request(method=RequestMethod.PUT, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self
