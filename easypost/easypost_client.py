from easypost.constant import (
    API_BASE,
    TIMEOUT,
)
from easypost.services.address_service import AddressService


class EasyPostClient:
    """A client object used to authenticate and configure all HTTP calls to the EasyPost API."""

    def __init__(self, api_key: str, api_base: str = API_BASE, timeout: int = TIMEOUT):
        # Client configuration
        self.api_key = api_key
        self.api_base = api_base
        self.timeout = timeout

        # Services
        self.address = AddressService(self)
