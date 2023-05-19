# flake8: noqa
from easypost.constant import (
    AUTHOR,
    VERSION,
    VERSION_INFO,
)
from easypost.easypost_client import EasyPostClient
from easypost.util import (
    get_lowest_object_rate,
    get_lowest_smart_rate,
    get_lowest_stateless_rate,
    receive_event,
    validate_webhook,
)


__author__ = AUTHOR
__version__ = VERSION
version_info = VERSION_INFO
