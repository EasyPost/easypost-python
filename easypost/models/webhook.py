from datetime import datetime
from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Webhook(EasyPostObject):
    disabled_at: Optional[datetime] = Field(None, alias="disabled_at")
    url: Optional[str] = Field(None, alias="url")
