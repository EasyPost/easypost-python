from datetime import datetime
from typing import Optional

from easypost.easypost_object import EasyPostObject
from easypost.models.tracking_location import TrackingLocation
from pydantic import Field


class TrackingDetail(EasyPostObject):
    date_time: Optional[datetime] = Field(None, alias="datetime")
    message: Optional[str] = Field(None, alias="message")
    source: Optional[str] = Field(None, alias="source")
    status: Optional[str] = Field(None, alias="status")
    status_detail: Optional[str] = Field(None, alias="status_detail")
    tracking_location: Optional[TrackingLocation] = Field(None, alias="tracking_location")
