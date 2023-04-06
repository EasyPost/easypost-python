import json
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)


class Error(Exception):
    def __init__(
        self,
        message: Optional[
            Union[Dict[str, Any], list, str]
        ] = None,  # message should be a string but can sometimes incorrectly come back as a list
        http_status: Optional[int] = None,
        http_body: Optional[Union[str, bytes]] = None,
        original_exception: Optional[Exception] = None,
    ):
        super(Error, self).__init__(message)
        message_list: List[str] = []
        Error.traverse_json_element(message, message_list)
        self.message = ", ".join(message_list)
        self.http_status = http_status
        self.http_body = http_body
        self.original_exception = original_exception
        # TODO: add missing `errors` param among others in thread-safe rewrite and update tests

        if http_body:
            try:
                self.json_body = json.loads(http_body)
            except Exception:
                self.json_body = None

        try:
            self.param = self.json_body["error"].get("param", None)
        except Exception:
            self.param = None

    @staticmethod
    def traverse_json_element(
        error_message: Optional[Union[Dict[str, Any], list, str]], messages_list: List[str]
    ) -> None:
        """Recursively traverses a JSON object or array and extracts error messages
        as strings. Adds the extracted messages to the specified messages_list array.
        """
        if isinstance(error_message, dict):
            for value in error_message.values():
                Error.traverse_json_element(value, messages_list)
        elif isinstance(error_message, list):
            for value in error_message:
                Error.traverse_json_element(value, messages_list)
        else:
            messages_list.append(str(error_message))
