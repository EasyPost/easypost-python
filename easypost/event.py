import json

import easypost
from easypost.easypost_object import convert_to_easypost_object
from easypost.resource import AllResource, Resource


class Event(AllResource, Resource):
    @classmethod
    def receive(cls, values):
        return convert_to_easypost_object(json.loads(values), easypost.api_key)
