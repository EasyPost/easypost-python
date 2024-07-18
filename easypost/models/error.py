from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Error(EasyPostObject):
    code: Optional[str] = Field(None, alias="code")
    errors: Optional[List["Error"]] = Field(None, alias="errors")
    field: Optional[str] = Field(None, alias="field")
    suggestion: Optional[str] = Field(None, alias="suggestion")
    raw_message: Optional[object] = Field(None, alias="message")

    @property
    def message(self):
        # This parses the message from the API response and returns it as a string regardless of what type it
        # actually is.
        messages = self.collect_error_messages(self.raw_message, [])
        if len(messages) == 0:
            return None
        elif len(messages) == 1:
            return messages[0]
        else:
            return ", ".join(messages)

    @staticmethod
    def _collect_error_messages(element, collected_messages):
        if element is None:
            return collected_messages
        elif isinstance(element, list):
            for item in element:
                collected_messages = Error.collect_error_messages(item, collected_messages)
        elif isinstance(element, dict):
            for value in element.values():
                collected_messages = Error.collect_error_messages(value, collected_messages)
        else:
            as_string = str(element)
            if as_string.strip():
                collected_messages.append(as_string)
        return collected_messages
