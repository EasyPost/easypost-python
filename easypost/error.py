import json


class Error(Exception):
    def __init__(self, message=None, http_status=None, http_body=None, original_exception=None):
        super(Error, self).__init__(message)
        self.message = message
        self.http_status = http_status
        self.http_body = http_body
        self.original_exception = original_exception
        try:
            self.json_body = json.loads(http_body)
        except Exception:
            self.json_body = None

        self.param = None
        try:
            self.param = self.json_body["error"].get("param", None)
        except Exception:
            pass
