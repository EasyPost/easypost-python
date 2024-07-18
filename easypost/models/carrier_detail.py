from datetime import datetime
from typing import Optional

from easypost.easypost_object import EasyPostObject
from easypost.models.tracking_location import TrackingLocation
from pydantic import Field


class CarrierDetail(EasyPostObject):
    alternate_identifier: Optional[str] = Field(None, alias="alternate_identifier")
    container_type: Optional[str] = Field(None, alias="container_type")
    destination_location: Optional[str] = Field(None, alias="destination_location")
    destination_tracking_location: Optional[TrackingLocation] = Field(None, alias="destination_tracking_location")
    est_delivery_date_local: Optional[str] = Field(None, alias="est_delivery_date_local")
    est_delivery_time_local: Optional[str] = Field(None, alias="est_delivery_time_local")
    guaranteed_delivery_date: Optional[datetime] = Field(None, alias="guaranteed_delivery_date")
    initial_delivery_attempt: Optional[datetime] = Field(None, alias="initial_delivery_attempt")
    origin_location: Optional[str] = Field(None, alias="origin_location")
    origin_tracking_location: Optional[TrackingLocation] = Field(None, alias="origin_tracking_location")
    service: Optional[str] = Field(None, alias="service")
