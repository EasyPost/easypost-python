from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class TrackingLocation(EasyPostObject):
    city: Optional[str] = Field(None, alias="city")
    country: Optional[str] = Field(None, alias="country")
    state: Optional[str] = Field(None, alias="state")
    zip: Optional[str] = Field(None, alias="zip")
