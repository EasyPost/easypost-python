from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Message(EasyPostObject):
    carrier: Optional[str] = Field(None, alias="carrier")
    carrier_account_id: Optional[str] = Field(None, alias="carrier_account_id")
    text: Optional[str] = Field(None, alias="text")
    type: Optional[str] = Field(None, alias="type")
