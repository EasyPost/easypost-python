from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.models.customs_item import CustomsItem
from pydantic import Field


class CustomsInfo(EasyPostObject):
    contents_explanation: Optional[str] = Field(None, alias="contents_explanation")
    contents_type: Optional[str] = Field(None, alias="contents_type")
    customs_certify: Optional[bool] = Field(None, alias="customs_certify")
    customs_items: Optional[List[CustomsItem]] = Field(None, alias="customs_items")
    customs_signer: Optional[str] = Field(None, alias="customs_signer")
    declaration: Optional[str] = Field(None, alias="declaration")
    eel_pfc: Optional[str] = Field(None, alias="eel_pfc")
    non_delivery_option: Optional[str] = Field(None, alias="non_delivery_option")
    restriction_comments: Optional[str] = Field(None, alias="restriction_comments")
    restriction_type: Optional[str] = Field(None, alias="restriction_type")
