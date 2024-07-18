from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class PickupRate(EasyPostObject):
    pickup_id: Optional[str] = Field(None, alias="pickup_id")
