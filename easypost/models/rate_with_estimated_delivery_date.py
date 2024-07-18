from datetime import datetime
from typing import Optional

from easypost.easypost_object import EasyPostObject
from easypost.models.rate import Rate
from easypost.models.time_in_transit import TimeInTransit
from pydantic import Field


class TimeInTransitDetails(EasyPostObject):
    days_in_transit: Optional[TimeInTransit] = Field(None, alias="days_in_transit")
    estimated_delivery_date: Optional[datetime] = Field(None, alias="easypost_estimated_delivery_date")
    planned_ship_date: Optional[datetime] = Field(None, alias="planned_ship_date")


class RateWithEstimatedDeliveryDate(EasyPostObject):
    rate: Optional[Rate] = Field(None, alias="rate")
    time_in_transit_details: Optional[TimeInTransitDetails] = Field(None, alias="easypost_time_in_transit_data")
