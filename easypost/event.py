import json
from typing import (
    List,
    Optional,
)

import easypost
from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    AllResource,
    NextPageResource,
)


class Event(AllResource, NextPageResource):
    @classmethod
    def receive(cls, values: str) -> "Event":
        return convert_to_easypost_object(response=json.loads(s=values), api_key=easypost.api_key)

    @classmethod
    def retrieve_all_payloads(cls, event_id: str, api_key: Optional[str] = None, **params) -> List["easypost.Payload"]:
        """Retrieve a list of Payloads for an Event."""
        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{event_id}/payloads"
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)
        return convert_to_easypost_object(response=response, api_key=api_key)

    @classmethod
    def retrieve_payload(
        cls, event_id: str, payload_id: str, api_key: Optional[str] = None, **params
    ) -> "easypost.Payload":
        """Retrieve a Payload of an Event."""
        requestor = Requestor(local_api_key=api_key)
        url = f"{cls.class_url()}/{event_id}/payloads/{payload_id}"
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)
        return convert_to_easypost_object(response=response, api_key=api_key)
