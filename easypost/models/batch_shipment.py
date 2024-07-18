from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class BatchShipment(EasyPostObject):
    batch_message: Optional[str] = Field(None, alias="batch_message")
    batch_status: Optional[str] = Field(None, alias="batch_status")
    tracking_code: Optional[str] = Field(None, alias="tracking_code")
