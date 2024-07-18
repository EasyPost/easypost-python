from datetime import datetime
from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from pydantic import Field


class Report(EasyPostObject):
    end_date: Optional[datetime] = Field(None, alias="end_date")
    include_children: Optional[bool] = Field(None, alias="include_children")
    start_date: Optional[datetime] = Field(None, alias="start_date")
    status: Optional[str] = Field(None, alias="status")
    url: Optional[str] = Field(None, alias="url")
    url_expiration: Optional[datetime] = Field(None, alias="url_expires_at")


class ReportCollection(PaginatedCollection):
    reports: List[Report] = Field([], alias="reports")
