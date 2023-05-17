# flake8: noqa
VERSION = "7.13.0"
VERSION_INFO = [str(number) for number in VERSION.split(".")]
API_BASE = "https://api.easypost.com/v2"
TIMEOUT = 60

SUPPORT_EMAIL = "support@easypost.com"

_CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS = [
    "FedexAccount",
    "UpsAccount",
]
