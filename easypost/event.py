import json

import easypost
from easypost.easypost_object import convert_to_easypost_object
from easypost.resource import (
    AllResource,
    Resource,
)


class Event(AllResource, Resource):
    @classmethod
    def receive(cls, values: str) -> "Event":
        return convert_to_easypost_object(response=json.loads(s=values), api_key=easypost.api_key)
