from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from easypost.errors.api.api_error import ApiError


class EncodingError(ApiError):
    def __init__(
        self,
        message: Union[
            Dict[str, Any], list, str
        ],  # message should be a string but can sometimes incorrectly come back as a list or object
        errors: Optional[List[str]] = None,
        code: Optional[str] = None,
        http_status: Optional[int] = None,
        http_body: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(
            message=message,
            errors=errors,
            code=code,
            http_status=http_status,
            http_body=http_body,
        )
