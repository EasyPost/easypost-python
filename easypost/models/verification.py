from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.models.error import Error
from easypost.models.verification_details import VerificationDetails
from pydantic import Field


class Verification(EasyPostObject):
    details: Optional[VerificationDetails] = Field(None, alias="details")
    errors: Optional[List[Error]] = Field(None, alias="errors")
    success: Optional[bool] = Field(None, alias="success")
