from datetime import datetime
from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from easypost.models.carrier_detail import CarrierDetail
from easypost.models.fee import Fee
from easypost.models.tracking_detail import TrackingDetail
from pydantic import Field


class Tracker(EasyPostObject):
    carrier: Optional[str] = Field(None, alias="carrier")
    carrier_detail: Optional[CarrierDetail] = Field(None, alias="carrier_detail")
    est_delivery_date: Optional[datetime] = Field(None, alias="est_delivery_date")
    fees: Optional[List[Fee]] = Field(None, alias="fees")
    public_url: Optional[str] = Field(None, alias="public_url")
    shipment_id: Optional[str] = Field(None, alias="shipment_id")
    signed_by: Optional[str] = Field(None, alias="signed_by")
    status: Optional[str] = Field(None, alias="status")
    status_detail: Optional[str] = Field(None, alias="status_detail")
    tracking_code: Optional[str] = Field(None, alias="tracking_code")
    tracking_details: Optional[List[TrackingDetail]] = Field(None, alias="tracking_details")
    tracking_updated_at: Optional[datetime] = Field(None, alias="tracking_updated_at")
    weight: Optional[float] = Field(None, alias="weight")


class TrackerCollection(PaginatedCollection):
    trackers: list[Tracker] = Field([], alias="trackers")
