from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from pydantic import Field


class EndShipper(EasyPostObject):
    city: Optional[str] = Field(None, alias="city")
    company: Optional[str] = Field(None, alias="company")
    country: Optional[str] = Field(None, alias="country")
    email: Optional[str] = Field(None, alias="email")
    error: Optional[str] = Field(None, alias="error")
    message: Optional[str] = Field(None, alias="message")
    name: Optional[str] = Field(None, alias="name")
    phone: Optional[str] = Field(None, alias="phone")
    state: Optional[str] = Field(None, alias="state")
    street1: Optional[str] = Field(None, alias="street1")
    street2: Optional[str] = Field(None, alias="street2")
    zip: Optional[str] = Field(None, alias="zip")


class EndShipperCollection(PaginatedCollection):
    end_shippers: List[EndShipper] = Field([], alias="end_shippers")
