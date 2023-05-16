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
from easypost.services.event_service import EventService
from easypost.services.insurance_service import InsuranceService
from easypost.services.order_service import OrderService
from easypost.services.parcel_service import ParcelService
from easypost.services.pickup_service import PickupService
from easypost.services.rate_service import RateService
from easypost.services.referral_customer_service import ReferralCustomerService
from easypost.services.refund_service import RefundService
from easypost.services.report_service import ReportService
from easypost.services.scan_form_service import ScanFormService


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
        self.event = EventService(self)
        self.insurance = InsuranceService(self)
        self.order = OrderService(self)
        self.parcel = ParcelService(self)
        self.rate = RateService(self)
        self.pickup = PickupService(self)
        self.referral_customer = ReferralCustomerService(self)
        self.refund = RefundService(self)
        self.report = ReportService(self)
        self.scan_form = ScanFormService(self)
