from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Parcel(EasyPostObject):
    height: Optional[float] = Field(None, alias="height")
    length: Optional[float] = Field(None, alias="length")
    predefined_package: Optional[str] = Field(None, alias="predefined_package")
    weight: Optional[float] = Field(None, alias="weight")
    width: Optional[float] = Field(None, alias="width")
