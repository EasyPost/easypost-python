from easypost.constant import (
    API_BASE,
    TIMEOUT,
)
from easypost.services.address_service import AddressService
from easypost.services.batch_service import BatchService
from easypost.services.beta_carrier_metadata_service import BetaCarrierMetadataService
from easypost.services.beta_rate_service import BetaRateService
from easypost.services.beta_referral_customer_service import BetaReferralCustomerService
from easypost.services.billing_service import BillingService
from easypost.services.carrier_account_service import CarrierAccountService
from easypost.services.customs_info_service import CustomsInfoService
from easypost.services.customs_item_service import CustomsItemService
from easypost.services.end_shipper_service import EndShipperService


class EasyPostClient:
    """A client object used to authenticate and configure all HTTP calls to the EasyPost API."""

    def __init__(self, api_key: str, api_base: str = API_BASE, timeout: int = TIMEOUT):
        # Client configuration
        self.api_key = api_key
        self.api_base = api_base
        self.timeout = timeout

        # Services
        self.address = AddressService(self)
        self.batch = BatchService(self)
        self.beta_carrier_metadata = BetaCarrierMetadataService(self)
        self.beta_rate = BetaRateService(self)
        self.beta_referral_customer = BetaReferralCustomerService(self)
        self.billing = BillingService(self)
        self.carrier_account = CarrierAccountService(self)
        self.customs_info = CustomsInfoService(self)
        self.customs_item = CustomsItemService(self)
        self.end_shipper = EndShipperService(self)
