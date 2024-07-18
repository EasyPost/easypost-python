from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Fee(EasyPostObject):
    amount: Optional[float] = Field(None, alias="amount")
    charged: Optional[bool] = Field(None, alias="charged")
    refunded: Optional[bool] = Field(None, alias="refunded")
    type: Optional[str] = Field(None, alias="type")
