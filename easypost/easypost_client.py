from easypost.constant import (
    API_BASE,
    TIMEOUT,
)
from easypost.services import (
    AddressService,
    BatchService,
    BetaCarrierMetadataService,
    BetaRateService,
    BetaReferralCustomerService,
    BillingService,
    CarrierAccountService,
    CustomsInfoService,
    CustomsItemService,
    EndShipperService,
    EventService,
    InsuranceService,
    OrderService,
    ParcelService,
    PickupService,
    RateService,
    ReferralCustomerService,
    RefundService,
    ReportService,
    ScanFormService,
    ShipmentService,
    TrackerService,
    UserService,
    WebhookService,
)


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
        self.shipment = ShipmentService(self)
        self.tracker = TrackerService(self)
        self.user = UserService(self)
        self.webhook = WebhookService(self)
