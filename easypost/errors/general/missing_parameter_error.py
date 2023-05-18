from easypost.errors import EasyPostError


class MissingParameterError(EasyPostError):
    def __init__(self, message):
        super().__init__(message=message)
