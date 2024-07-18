from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class CustomsItem(EasyPostObject):
    code: Optional[str] = Field(None, alias="code")
    currency: Optional[str] = Field(None, alias="currency")
    description: Optional[str] = Field(None, alias="description")
    hs_tariff_number: Optional[str] = Field(None, alias="hs_tariff_number")
    origin_country: Optional[str] = Field(None, alias="origin_country")
    quantity: Optional[int] = Field(None, alias="quantity")
    value: Optional[float] = Field(None, alias="value")
    weight: Optional[float] = Field(None, alias="weight")
