class EasyPostError(Exception):
    """The base error that all other errors from EasyPost inherit."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
