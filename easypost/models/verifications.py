from typing import Optional

from easypost.easypost_object import EasyPostObject
from easypost.models.verification import Verification
from pydantic import Field


class Verifications(EasyPostObject):
    delivery: Optional[Verification] = Field(None, alias="delivery")
    zip: Optional[Verification] = Field(None, alias="zip")
