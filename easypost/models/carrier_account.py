from typing import (
    Dict,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.models.carrier_fields import CarrierFields
from pydantic import Field


class CarrierAccount(EasyPostObject):
    billing_type: Optional[str] = Field(None, alias="billing_type")
    clone: Optional[bool] = Field(None, alias="clone")
    credentials: Optional[Dict[str, object]] = Field(None, alias="credentials")
    description: Optional[str] = Field(None, alias="description")
    fields: Optional[CarrierFields] = Field(None, alias="fields")
    readable: Optional[str] = Field(None, alias="readable")
    reference: Optional[str] = Field(None, alias="reference")
    test_credentials: Optional[Dict[str, object]] = Field(None, alias="test_credentials")
    type: Optional[str] = Field(None, alias="type")
