from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class CarrierField(EasyPostObject):
    key: Optional[str] = Field(None, alias="key")
    visibility: Optional[str] = Field(None, alias="visibility")
    label: Optional[str] = Field(None, alias="label")
    value: Optional[str] = Field(None, alias="value")


class CarrierFields(EasyPostObject):
    credentials: Optional[CarrierField] = Field(None, alias="credentials")
    test_credentials: Optional[CarrierField] = Field(None, alias="test_credentials")
    auto_link: Optional[bool] = Field(None, alias="auto_link")
    custom_workflow: Optional[bool] = Field(None, alias="custom_workflow")
