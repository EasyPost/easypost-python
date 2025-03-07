import json
from typing import (
    Any,
    Optional,
    Union,
)

from easypost.errors.general.easypost_error import EasyPostError


class ApiError(EasyPostError):
    """Base error for all errors thrown via the EasyPost API."""

    def __init__(
        self,
        message: Union[
            dict[str, Any], list, str
        ],  # message should be a string but can sometimes incorrectly come back as a list or object
        errors: Optional[list[str]] = None,
        code: Optional[str] = None,
        http_status: Optional[int] = None,
        http_body: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(message)  # type: ignore
        message_list: list[str] = []
        self._traverse_json_element(message, message_list)
        self.message = ", ".join(message_list)
        self.errors = errors
        self.code = code
        self.http_status = http_status
        self.http_body = http_body

        if http_body:
            # Setup `json_body` property
            try:
                self.json_body = json.loads(http_body)
            except Exception:
                self.json_body = None

            if self.json_body is not None:
                # Setup `errors` property
                try:
                    self.errors = self.json_body["error"]["errors"]
                except Exception:
                    self.errors = None

                # Setup `code` property
                try:
                    self.code = self.json_body["error"]["code"]
                except Exception:
                    self.code = None

    def _traverse_json_element(
        self,
        error_message: Optional[Union[dict[str, Any], list, str]],
        messages_list: list[str],
    ) -> None:
        """Recursively traverses a JSON object or array and extracts error messages
        as strings. Adds the extracted messages to the specified messages_list array.
        """
        if isinstance(error_message, dict):
            for value in error_message.values():
                self._traverse_json_element(value, messages_list)
        elif isinstance(error_message, list):
            for value in error_message:
                self._traverse_json_element(value, messages_list)
        else:
            messages_list.append(str(error_message))
