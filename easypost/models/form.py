from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Form(EasyPostObject):
    form_type: Optional[str] = Field(None, alias="form_type")
    form_url: Optional[str] = Field(None, alias="form_url")
    submitted_electronically: Optional[bool] = Field(None, alias="submitted_electronically")
