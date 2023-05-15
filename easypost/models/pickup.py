from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.util import get_lowest_object_rate


class Pickup(EasyPostObject):
    def lowest_rate(self, carriers: Optional[List[str]] = None, services: Optional[List[str]] = None):
        """Get the lowest rate of this Pickup."""
        lowest_rate = get_lowest_object_rate(self, carriers, services)

        return lowest_rate
