from typing import (
    Dict,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class CarrierType(EasyPostObject):
    fields: Optional[Dict[str, any]] = Field(None, alias="fields")
    logo: Optional[str] = Field(None, alias="logo")
    readable: Optional[str] = Field(None, alias="readable")
    type: Optional[str] = Field(None, alias="type")
