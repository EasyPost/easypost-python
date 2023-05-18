from easypost.errors import ApiError


class UnauthorizedError(ApiError):
    def __init__(self, message, errors, code, http_status, http_body):
        super().__init__(
            message=message,
            errors=errors,
            code=code,
            http_status=http_status,
            http_body=http_body,
        )
