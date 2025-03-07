from typing import (
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.models.rate import Rate
from easypost.util import get_lowest_object_rate


class Order(EasyPostObject):
    def lowest_rate(self, carriers: Optional[list[str]] = None, services: Optional[list[str]] = None) -> Rate:
        """Get the lowest rate of this Order."""
        lowest_rate = get_lowest_object_rate(self, carriers, services)

        return lowest_rate
