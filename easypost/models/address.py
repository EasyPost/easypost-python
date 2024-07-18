from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from easypost.models.verifications import Verifications
from pydantic import Field


class Address(EasyPostObject):
    carrier_facility: Optional[str] = Field(None, alias="carrier_facility")
    city: Optional[str] = Field(None, alias="city")
    company: Optional[str] = Field(None, alias="company")
    country: Optional[str] = Field(None, alias="country")
    email: Optional[str] = Field(None, alias="email")
    error: Optional[str] = Field(None, alias="error")
    federal_tax_id: Optional[str] = Field(None, alias="federal_tax_id")
    message: Optional[str] = Field(None, alias="message")
    name: Optional[str] = Field(None, alias="name")
    phone: Optional[str] = Field(None, alias="phone")
    residential: Optional[bool] = Field(None, alias="residential")
    state: Optional[str] = Field(None, alias="state")
    state_tax_id: Optional[str] = Field(None, alias="state_tax_id")
    street1: Optional[str] = Field(None, alias="street1")
    street2: Optional[str] = Field(None, alias="street2")
    verifications: Optional[Verifications] = Field(None, alias="verifications")
    zip: Optional[str] = Field(None, alias="zip")


class AddressCollection(PaginatedCollection):
    addresses: List[Address] = Field([], alias="addresses")
