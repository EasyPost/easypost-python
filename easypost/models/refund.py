from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from pydantic import Field


class Refund(EasyPostObject):
    carrier: Optional[str] = Field(None, alias="carrier")
    confirmation_number: Optional[str] = Field(None, alias="confirmation_number")
    shipment_id: Optional[str] = Field(None, alias="shipment_id")
    status: Optional[str] = Field(None, alias="status")
    tracking_code: Optional[str] = Field(None, alias="tracking_code")


class RefundCollection(PaginatedCollection):
    refunds: List[Refund] = Field([], alias="refunds")
