from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from easypost.models.api_key import ApiKey
from pydantic import Field


class User(EasyPostObject):
    api_keys: Optional[List[ApiKey]] = Field(None, alias="api_keys")
    balance: Optional[str] = Field(None, alias="balance")
    children: Optional[List["User"]] = Field(None, alias="children")
    email: Optional[str] = Field(None, alias="email")
    name: Optional[str] = Field(None, alias="name")
    parent_id: Optional[str] = Field(None, alias="parent_id")
    password: Optional[str] = Field(None, alias="password")
    password_confirmation: Optional[str] = Field(None, alias="password_confirmation")
    phone_number: Optional[str] = Field(None, alias="phone_number")
    price_per_shipment: Optional[str] = Field(None, alias="price_per_shipment")
    recharge_amount: Optional[str] = Field(None, alias="recharge_amount")
    recharge_threshold: Optional[str] = Field(None, alias="recharge_threshold")
    secondary_recharge_amount: Optional[str] = Field(None, alias="secondary_recharge_amount")
    convenience_fee_rate: Optional[str] = Field(None, alias="cc_fee_rate")
    insurance_fee_rate: Optional[str] = Field(None, alias="insurance_fee_rate")
    insurance_fee_minimum: Optional[str] = Field(None, alias="insurance_fee_minimum")
    verified: Optional[bool] = Field(None, alias="verified")


class ChildUserCollection(PaginatedCollection):
    children: List[User] = Field([], alias="children")
