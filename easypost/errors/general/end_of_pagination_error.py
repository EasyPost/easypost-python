from easypost.errors import EasyPostError


class EndOfPaginationError(EasyPostError):
    def __init__(self, message: str):
        super().__init__(message=message)
