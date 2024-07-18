from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.models.address import Address
from easypost.models.carrier_account import CarrierAccount
from easypost.models.customs_info import CustomsInfo
from easypost.models.message import Message
from easypost.models.rate import Rate
from easypost.models.shipment import Shipment
from easypost.util import get_lowest_object_rate
from pydantic import Field


class Order(EasyPostObject):
    buyer_address: Optional[Address] = Field(None, alias="buyer_address")
    carrier_accounts: Optional[List[CarrierAccount]] = Field(None, alias="carrier_accounts")
    customs_info: Optional[CustomsInfo] = Field(None, alias="customs_info")
    from_address: Optional[Address] = Field(None, alias="from_address")
    is_return: Optional[bool] = Field(None, alias="is_return")
    messages: Optional[List[Message]] = Field(None, alias="messages")
    rates: Optional[List[Rate]] = Field(None, alias="rates")
    reference: Optional[str] = Field(None, alias="reference")
    return_address: Optional[Address] = Field(None, alias="return_address")
    service: Optional[str] = Field(None, alias="service")
    shipments: Optional[List[Shipment]] = Field(None, alias="shipments")
    to_address: Optional[Address] = Field(None, alias="to_address")

    def lowest_rate(self, carriers: Optional[List[str]] = None, services: Optional[List[str]] = None) -> Rate:
        """Get the lowest rate of this Order."""
        lowest_rate = get_lowest_object_rate(self, carriers, services)

        return lowest_rate
