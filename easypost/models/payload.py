from typing import (
    Dict,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Payload(EasyPostObject):
    request_url: Optional[str] = Field(None, alias="request_url")
    request_headers: Optional[Dict[str, str]] = Field(None, alias="request_headers")
    request_body: Optional[str] = Field(None, alias="request_body")
    response_headers: Optional[Dict[str, str]] = Field(None, alias="response_headers")
    response_body: Optional[str] = Field(None, alias="response_body")
    response_code: Optional[int] = Field(None, alias="response_code")
    total_time: Optional[float] = Field(None, alias="total_time")
