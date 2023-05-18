from easypost.errors import EasyPostError


class SignatureVerificationError(EasyPostError):
    def __init__(self, message: str):
        super().__init__(message=message)
