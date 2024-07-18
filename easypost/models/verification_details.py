from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class VerificationDetails(EasyPostObject):
    latitude: Optional[float] = Field(None, alias="latitude")
    longitude: Optional[float] = Field(None, alias="longitude")
    time_zone: Optional[str] = Field(None, alias="time_zone")
