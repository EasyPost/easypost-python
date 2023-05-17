# flake8: noqa
VERSION = "7.13.0"
VERSION_INFO = [str(number) for number in VERSION.split(".")]

API_BASE = "https://api.easypost.com"
API_VERSION = "v2"
SUPPORT_EMAIL = "support@easypost.com"
TIMEOUT = 60

_CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS = [
    "FedexAccount",
    "UpsAccount",
]
