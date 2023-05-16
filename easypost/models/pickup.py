from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.models.rate import Rate
from easypost.util import get_lowest_object_rate


class Pickup(EasyPostObject):
    def lowest_rate(self, carriers: Optional[List[str]] = None, services: Optional[List[str]] = None) -> Rate:
        """Get the lowest rate of this Pickup."""
        lowest_rate = get_lowest_object_rate(self, carriers, services, "pickup_rates")

        return lowest_rate
