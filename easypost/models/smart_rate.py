from datetime import datetime
from typing import Optional

from easypost.easypost_object import EasyPostObject
from easypost.models.time_in_transit import TimeInTransit
from pydantic import Field


class SmartRate(EasyPostObject):
    billing_type: Optional[str] = Field(None, alias="billing_type")
    carrier: Optional[str] = Field(None, alias="carrier")
    carrier_account_id: Optional[str] = Field(None, alias="carrier_account_id")
    currency: Optional[str] = Field(None, alias="currency")
    delivery_date: Optional[datetime] = Field(None, alias="delivery_date")
    delivery_date_guaranteed: Optional[bool] = Field(None, alias="delivery_date_guaranteed")
    delivery_days: Optional[int] = Field(None, alias="delivery_days")
    est_delivery_days: Optional[int] = Field(None, alias="est_delivery_days")
    list_currency: Optional[str] = Field(None, alias="list_currency")
    list_rate: Optional[str] = Field(None, alias="list_rate")
    rate: Optional[float] = Field(None, alias="rate")
    retail_currency: Optional[str] = Field(None, alias="retail_currency")
    retail_rate: Optional[str] = Field(None, alias="retail_rate")
    service: Optional[str] = Field(None, alias="service")
    shipment_id: Optional[str] = Field(None, alias="shipment_id")
    time_in_transit: Optional[TimeInTransit] = Field(None, alias="time_in_transit")
