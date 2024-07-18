import datetime
from typing import Dict
from uuid import UUID

from easypost.hooks import EventHook


class RequestHook(EventHook):
    """An event that gets triggered when an HTTP request begins."""

    method: str
    path: str
    headers: Dict[str, str]
    request_body: Dict[str, str]
    request_timestamp: datetime.datetime
    request_uuid: UUID
