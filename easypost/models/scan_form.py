from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from easypost.models.address import Address
from pydantic import Field


class ScanForm(EasyPostObject):
    address: Optional[Address] = Field(None, alias="address")
    batch_id: Optional[str] = Field(None, alias="batch_id")
    form_file_type: Optional[str] = Field(None, alias="form_file_type")
    form_url: Optional[str] = Field(None, alias="form_url")
    message: Optional[str] = Field(None, alias="message")
    status: Optional[str] = Field(None, alias="status")
    tracking_codes: Optional[List[str]] = Field(None, alias="tracking_codes")


class ScanFormCollection(PaginatedCollection):
    scan_forms: List[ScanForm] = Field([], alias="scan_forms")
