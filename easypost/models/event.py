from typing import (
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from pydantic import Field


class Event(EasyPostObject):
    completed_urls: Optional[List[str]] = Field(None, alias="completed_urls")
    description: Optional[str] = Field(None, alias="description")
    pending_urls: Optional[List[str]] = Field(None, alias="pending_urls")
    previous_attributes: Optional[Dict[str, object]] = Field(None, alias="previous_attributes")
    result: Optional[Dict[str, object]] = Field(None, alias="result")
    status: Optional[str] = Field(None, alias="status")
    user_id: Optional[str] = Field(None, alias="user_id")


class EventCollection(PaginatedCollection):
    events: List[Event] = Field([], alias="events")
