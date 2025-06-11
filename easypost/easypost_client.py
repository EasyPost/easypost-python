from easypost.constant import (
    API_BASE,
    API_VERSION,
    INVALID_REQUESTS_VERSION_ERROR,
    SUPPORT_EMAIL,
    TIMEOUT,
)
from easypost.hooks import (
    RequestHook,
    ResponseHook,
)
from easypost.services import (
    AddressService,
    ApiKeyService,
    BatchService,
    BetaRateService,
    BetaReferralCustomerService,
    BillingService,
    CarrierAccountService,
    CarrierMetadataService,
    ClaimService,
    CustomsInfoService,
    CustomsItemService,
    EndShipperService,
    EventService,
    InsuranceService,
    LumaService,
    OrderService,
    ParcelService,
    PickupService,
    RateService,
    ReferralCustomerService,
    RefundService,
    ReportService,
    ScanFormService,
    ShipmentService,
    SmartRateService,
    TrackerService,
    UserService,
    WebhookService,
)


class EasyPostClient:
    """A client object used to authenticate and configure all HTTP calls to the EasyPost API."""

    def __init__(
        self,
        api_key: str,
        api_base: str = f"{API_BASE}/{API_VERSION}",
        timeout: int = TIMEOUT,
    ):
        # Client configuration
        self.api_key = api_key
        self.api_base = api_base
        self.timeout = timeout

        # Services
        self.address = AddressService(self)
        self.api_keys = ApiKeyService(self)
        self.batch = BatchService(self)
        self.beta_rate = BetaRateService(self)
        self.beta_referral_customer = BetaReferralCustomerService(self)
        self.billing = BillingService(self)
        self.carrier_account = CarrierAccountService(self)
        self.carrier_metadata = CarrierMetadataService(self)
        self.claim = ClaimService(self)
        self.customs_info = CustomsInfoService(self)
        self.customs_item = CustomsItemService(self)
        self.end_shipper = EndShipperService(self)
        self.event = EventService(self)
        self.insurance = InsuranceService(self)
        self.luma = LumaService(self)
        self.order = OrderService(self)
        self.parcel = ParcelService(self)
        self.rate = RateService(self)
        self.pickup = PickupService(self)
        self.referral_customer = ReferralCustomerService(self)
        self.refund = RefundService(self)
        self.report = ReportService(self)
        self.scan_form = ScanFormService(self)
        self.shipment = ShipmentService(self)
        self.smart_rate = SmartRateService(self)
        self.tracker = TrackerService(self)
        self.user = UserService(self)
        self.webhook = WebhookService(self)

        # Hooks
        self._request_hook = RequestHook()
        self._response_hook = ResponseHook()

        # use urlfetch as request_lib on google app engine, otherwise use requests
        self._request_lib = None
        try:
            from google.appengine.api import urlfetch  # type: ignore

            self._request_lib = "urlfetch"
            # use the GAE application-wide "deadline" (or its default)
            timeout = urlfetch.get_default_fetch_deadline() or self.timeout
        except ImportError:
            try:
                import requests

                self._request_lib = "requests"
                self._requests_session = requests.Session()
                requests_http_adapter = requests.adapters.HTTPAdapter(max_retries=3)
                self._requests_session.mount(
                    prefix=self.api_base.split(f"/{API_VERSION}")[0],
                    adapter=requests_http_adapter,
                )
            except Exception:
                raise ImportError(INVALID_REQUESTS_VERSION_ERROR.format(SUPPORT_EMAIL))

            try:
                requests_version = requests.__version__
                major_version, _, _ = [int(i) for i in requests_version.split(".")]
            except Exception:
                raise ImportError(INVALID_REQUESTS_VERSION_ERROR.format(SUPPORT_EMAIL))
            else:
                if major_version < 1:
                    raise ImportError(INVALID_REQUESTS_VERSION_ERROR.format(SUPPORT_EMAIL))

    def subscribe_to_request_hook(self, function):
        """Subscribe functions to run when a request occurs."""
        self._request_hook += function

    def unsubscribe_from_request_hook(self, function):
        """Unsubscribe functions from running when a request occurs."""
        self._request_hook -= function

    def subscribe_to_response_hook(self, function):
        """Subscribe functions to run when a response occurs."""
        self._response_hook += function

    def unsubscribe_from_response_hook(self, function):
        """Unsubscribe functions from running when a response occurs."""
        self._response_hook -= function
