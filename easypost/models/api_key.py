from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class ApiKey(EasyPostObject):
    key: Optional[str] = Field(None, alias="key")


class ApiKeyCollection(EasyPostObject):
    children: Optional[List["ApiKeyCollection"]] = Field(None, alias="children")
    keys: List[ApiKey] = Field(None, alias="keys")
