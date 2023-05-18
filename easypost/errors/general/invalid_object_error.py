from easypost.errors import EasyPostError


class InvalidObjectError(EasyPostError):
    def __init__(self, message):
        super().__init__(message=message)
