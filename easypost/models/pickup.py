from datetime import datetime
from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.models.address import Address
from easypost.models.carrier_account import CarrierAccount
from easypost.models.message import Message
from easypost.models.pickup_rate import PickupRate
from easypost.models.rate import Rate
from easypost.util import get_lowest_object_rate
from pydantic import Field


class Pickup(EasyPostObject):
    address: Optional[Address] = Field(None, alias="address")
    carrier_accounts: Optional[List[CarrierAccount]] = Field(None, alias="carrier_accounts")
    confirmation: Optional[str] = Field(None, alias="confirmation")
    instructions: Optional[str] = Field(None, alias="instructions")
    is_account_address: Optional[bool] = Field(None, alias="is_account_address")
    max_datetime: Optional[datetime] = Field(None, alias="max_datetime")
    messages: Optional[List[Message]] = Field(None, alias="messages")
    min_datetime: Optional[datetime] = Field(None, alias="min_datetime")
    name: Optional[str] = Field(None, alias="name")
    pickup_rates: Optional[List[PickupRate]] = Field(None, alias="pickup_rates")
    reference: Optional[str] = Field(None, alias="reference")
    status: Optional[str] = Field(None, alias="status")

    def lowest_rate(self, carriers: Optional[List[str]] = None, services: Optional[List[str]] = None) -> Rate:
        """Get the lowest rate of this Pickup."""
        lowest_rate = get_lowest_object_rate(self, carriers, services, "pickup_rates")

        return lowest_rate
