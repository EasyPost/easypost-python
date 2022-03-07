import json

import easypost
import easypost.easypost_object as util
from easypost.resource import AllResource, Resource


class Event(AllResource, Resource):
    @classmethod
    def receive(cls, values):
        return util.convert_to_easypost_object(json.loads(values), easypost.api_key)
