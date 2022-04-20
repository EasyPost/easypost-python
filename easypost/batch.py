from typing import Optional

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    AllResource,
    CreateResource,
)


class Batch(AllResource, CreateResource):
    @classmethod
    def create_and_buy(cls, api_key: Optional[str] = None, **params) -> "Batch":
        """Create and buy a Batch."""
        requestor = Requestor(local_api_key=api_key)
        url = "%s/%s" % (cls.class_url(), "create_and_buy")
        wrapped_params = {cls.snakecase_name(): params}
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    def buy(self, **params) -> "Batch":
        """Buy a batch."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def label(self, **params) -> "Batch":
        """Create a batch label."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "label")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def remove_shipments(self, **params) -> "Batch":
        """Remove shipments from a batch."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "remove_shipments")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def add_shipments(self, **params) -> "Batch":
        """Add shipments from a batch."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "add_shipments")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    def create_scan_form(self, **params) -> "Batch":
        """Create a scanform for a batch."""
        requestor = Requestor(local_api_key=self._api_key)
        url = "%s/%s" % (self.instance_url(), "scan_form")
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self
