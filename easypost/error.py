import json
from typing import (
    Optional,
    Union,
)


class Error(Exception):
    def __init__(
        self,
        message: Optional[
            Union[str, list]
        ] = None,  # message should be a string but can sometimes incorrectly come back as a list
        http_status: Optional[int] = None,
        http_body: Optional[Union[str, bytes]] = None,
        original_exception: Optional[Exception] = None,
    ):
        super(Error, self).__init__(message)
        self.message = ", ".join(message) if type(message) == list else message
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
