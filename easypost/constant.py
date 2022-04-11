import platform

from .version import VERSION


SUPPORT_EMAIL = "support@easypost.com"
USER_AGENT = f"EasyPost/v2 PythonClient/{VERSION} Python/{platform.python_version()}"
TIMEOUT = 60
