from easypost.errors import EasyPostError


class FilteringError(EasyPostError):
    def __init__(self, message):
        super().__init__(message=message)
