from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from easypost.models.address import Address
from easypost.models.fee import Fee
from easypost.models.tracker import Tracker
from pydantic import Field


class Insurance(EasyPostObject):
    amount: Optional[str] = Field(None, alias="amount")
    from_address: Optional[Address] = Field(None, alias="from_address")
    messages: Optional[List[str]] = Field(None, alias="messages")
    provider: Optional[str] = Field(None, alias="provider")
    provider_id: Optional[str] = Field(None, alias="provider_id")
    reference: Optional[str] = Field(None, alias="reference")
    shipment_id: Optional[str] = Field(None, alias="shipment_id")
    status: Optional[str] = Field(None, alias="status")
    to_address: Optional[Address] = Field(None, alias="to_address")
    tracker: Optional[Tracker] = Field(None, alias="tracker")
    tracking_code: Optional[str] = Field(None, alias="tracking_code")
    fee: Optional[Fee] = Field(None, alias="fee")


class InsuranceCollection(PaginatedCollection):
    insurances: List[Insurance] = Field([], alias="insurances")
