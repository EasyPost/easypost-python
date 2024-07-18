import enum
import json
import platform
import time
import uuid
from datetime import (
    datetime,
    timezone,
)
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)
from urllib.parse import urlencode

import requests
from easypost.constant import (
    API_BASE,
    COMMUNICATION_ERROR,
    INVALID_REQUEST_LIB_ERROR,
    INVALID_REQUEST_METHOD_ERROR,
    INVALID_REQUEST_PARAMETERS_ERROR,
    INVALID_RESPONSE_BODY_ERROR,
    SUPPORT_EMAIL,
    TIMEOUT,
    TIMEOUT_ERROR,
    VERSION,
)
from easypost.easypost_object import EasyPostObject
from easypost.errors import (
    EasyPostError,
    HttpError,
    JsonError,
    RedirectError,
    UnknownApiError,
)
from easypost.hooks import (
    RequestHook,
    ResponseHook,
)
from easypost.http import HttpMethod
from easypost.requestor import STATUS_CODE_TO_ERROR_MAPPING
from easypost.services.address_service import AddressService
from easypost.services.api_key_service import ApiKeyService
from easypost.services.batch_service import BatchService
from easypost.services.beta_rate_service import BetaRateService
from easypost.services.beta_referral_customer_service import BetaReferralCustomerService
from easypost.services.billing_service import BillingService
from easypost.services.carrier_account_service import CarrierAccountService
from easypost.services.carrier_metadata_service import CarrierMetadataService
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
from easypost.services.shipment_service import ShipmentService
from easypost.services.tracker_service import TrackerService
from easypost.services.user_service import UserService
from easypost.services.webhook_service import WebhookService
from requests import JSONDecodeError


class ApiVersion(enum.Enum):
    Beta = "beta"
    V2 = "v2"


class RequestEngine(enum.Enum):
    URLFETCH = "urlfetch"
    REQUESTS = "requests"


class EasyPostClient:
    """A client object used to authenticate and configure all HTTP calls to the EasyPost API."""

    def __init__(
        self,
        api_key: str,
        api_base: str = API_BASE,
        api_version: ApiVersion = ApiVersion.V2,
        timeout: int = TIMEOUT,
    ):
        # Client configuration
        self.api_key: str = api_key
        self._api_base: str = api_base
        self._api_version: ApiVersion = api_version
        self.timeout: int = timeout

        # Services
        self.address: AddressService = AddressService(self)
        self.api_keys: ApiKeyService = ApiKeyService(self)
        self.batch: BatchService = BatchService(self)
        self.beta_rate: BetaRateService = BetaRateService(self)
        self.beta_referral_customer: BetaReferralCustomerService = BetaReferralCustomerService(self)
        self.billing: BillingService = BillingService(self)
        self.carrier_account: CarrierAccountService = CarrierAccountService(self)
        self.carrier_metadata: CarrierMetadataService = CarrierMetadataService(self)
        self.customs_info: CustomsInfoService = CustomsInfoService(self)
        self.customs_item: CustomsItemService = CustomsItemService(self)
        self.end_shipper: EndShipperService = EndShipperService(self)
        self.event: EventService = EventService(self)
        self.insurance: InsuranceService = InsuranceService(self)
        self.order: OrderService = OrderService(self)
        self.parcel: ParcelService = ParcelService(self)
        self.rate: RateService = RateService(self)
        self.pickup: PickupService = PickupService(self)
        self.referral_customer: ReferralCustomerService = ReferralCustomerService(self)
        self.refund: RefundService = RefundService(self)
        self.report: ReportService = ReportService(self)
        self.scan_form: ScanFormService = ScanFormService(self)
        self.shipment: ShipmentService = ShipmentService(self)
        self.tracker: TrackerService = TrackerService(self)
        self.user: UserService = UserService(self)
        self.webhook: WebhookService = WebhookService(self)

        # Hooks
        self._request_hook: RequestHook = RequestHook()
        self._response_hook: ResponseHook = ResponseHook()

        # use urlfetch as request_lib on google app engine, otherwise use requests
        self._request_engine: Optional[RequestEngine] = None
        self._requests_session: Optional[requests.Session] = None
        try:
            from google.appengine.api import urlfetch  # type: ignore

            self._request_engine = RequestEngine.URLFETCH
            # use the GAE application-wide "deadline" (or its default)
            self.timeout = urlfetch.get_default_fetch_deadline() or self.timeout
        except ImportError:
            try:
                import objectrest

                self._request_engine = RequestEngine.REQUESTS
                self._requests_session = requests.Session()
            except ImportError:
                raise ImportError(INVALID_REQUEST_LIB_ERROR.format(SUPPORT_EMAIL))

    @property
    def api_base_url(self):
        """Return the base URL for the EasyPost API."""
        return f"{self._api_base}/{self._api_version.value}"

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

    def _build_user_agent(self, api_version: ApiVersion) -> str:
        """Build the user agent string."""
        details = {
            "client_version": VERSION,
            "implementation": "NA",
            "os_arch": "NA",
            "os_version": "NA",
            "os": "NA",
            "python_version": "NA",
        }

        # Attempt to populate the user-agent header
        for attr, func in (
            ("implementation", platform.python_implementation),
            ("os_details", platform.uname),
            ("python_version", platform.python_version),
        ):
            try:
                val = func()  # type: ignore
                if attr == "os_details":
                    details["os"] = val[0]
                    details["os_version"] = val[2]
                    details["os_arch"] = val[4]
                else:
                    user_agent[attr] = val  # type: ignore
            except Exception:  # nosec
                # If we fail to get OS info, do nothing as we already set fallbacks for these values
                pass

        return (
            f"EasyPost/{api_version.value} PythonClient/{VERSION} Python/{details['python_version']}"  # type: ignore
            f" OS/{details['os']} OSVersion/{details['os_version']} OSArch/{details['os_arch']}"
            f" Implementation/{details['implementation']}"
        )

    def _build_headers(self, api_version: ApiVersion) -> Dict[str, str]:
        """Build the headers for the request."""
        return {"Authorization": f"Bearer {self.api_key}", "User-Agent": self._build_user_agent(api_version)}

    @classmethod
    def _objects_to_ids(cls, param: Dict[str, Any]) -> Dict[str, Any]:
        """If providing an object as a parameter to another object,
        only pass along the ID so the API will use the object reference correctly.
        """
        if isinstance(param, EasyPostObject):
            return {"id": param.id}
        elif isinstance(param, dict):
            data = {}
            for k, v in param.items():
                if isinstance(v, list):
                    data[k] = [cls._objects_to_ids(item) for item in v]  # type: ignore
                else:
                    data[k] = cls._objects_to_ids(v)  # type: ignore
            return data
        else:
            return param

    def _add_query_params_to_url(self, url: str, params: Dict[str, Any]) -> str:
        """Add query parameters to a URL."""
        if not params:
            return url

        converted_params = []

        for key, value in sorted(params.items()):
            if value is None:
                continue  # Don't add Nones to the query
            elif isinstance(value, datetime):
                value = int(time.mktime(value.timetuple()))  # to UTC timestamp
            converted_params.append((key, value))

        encoded_params = urlencode(query=converted_params)

        if encoded_params:
            return "%s?%s" % (url, encoded_params)

        return url

    def _request_with_urlfetch(
        self, method: HttpMethod, abs_url: str, headers: Dict[str, Any], params: Dict[str, Any]
    ) -> Tuple[str, int, Dict[str, Any]]:
        """Make a request by using the `urlfetch` library."""
        fetch_args = {
            "method": method.value,
            "headers": headers,
            "validate_certificate": False,
            "deadline": self.timeout,
        }

        if method in [HttpMethod.GET, HttpMethod.DELETE]:
            # GET/DELETE requests use query params
            fetch_args["url"] = self._add_query_params_to_url(url=abs_url, params=params)
        elif method in [HttpMethod.POST, HttpMethod.PUT]:
            fetch_args["url"] = abs_url
            # POST/PUT requests use body params
            fetch_args["payload"] = json.dumps(
                params, default=lambda v: v.decode("utf-8") if isinstance(v, bytes) else v
            )
        else:
            raise EasyPostError(INVALID_REQUEST_METHOD_ERROR.format(method, SUPPORT_EMAIL))

        try:
            from google.appengine.api import urlfetch  # type: ignore

            result = urlfetch.fetch(**fetch_args)  # type: ignore

            response_body: str = result.content
            response_status_code: int = result.status_code
            response_headers: dict[str, Any] = result.headers
        except Exception as e:
            raise HttpError(COMMUNICATION_ERROR.format(SUPPORT_EMAIL, e))

        return response_body, response_status_code, response_headers

    def _request_with_requests(
        self, method: HttpMethod, abs_url: str, headers: Dict[str, Any], params: Dict[str, Any]
    ) -> Tuple[str, int, Dict[str, Any]]:
        """Make a request by using the `request` library."""
        if method in [HttpMethod.GET, HttpMethod.DELETE]:
            request_query = params
            request_body = None
        elif method in [HttpMethod.POST, HttpMethod.PATCH, HttpMethod.PUT]:
            request_query = None
            request_body = params
        else:
            raise EasyPostError(INVALID_REQUEST_METHOD_ERROR.format(method, SUPPORT_EMAIL))

        if request_query and method not in [HttpMethod.GET, HttpMethod.DELETE]:
            raise EasyPostError(INVALID_REQUEST_PARAMETERS_ERROR)

        try:
            result = self._requests_session.request(
                method=method.value,
                url=abs_url,
                params=request_query,
                headers=headers,
                json=request_body,
                timeout=self.timeout,
                verify=True,
            )
            response_body: str = result.text
            response_status: int = result.status_code
            response_headers: dict[str, Any] = result.headers
        except requests.exceptions.Timeout:
            raise TimeoutError(TIMEOUT_ERROR)
        except Exception as e:
            raise HttpError(COMMUNICATION_ERROR.format(SUPPORT_EMAIL, e))

        return response_body, response_status, response_headers

    def _interpret_response(self, response_body: str, response_status: int) -> dict:
        if response_status == 204:
            # HTTP 204 does not have any response body and we can just return here
            return {}

        try:
            response_json = json.loads(response_body)
        except JSONDecodeError:
            raise JsonError(INVALID_RESPONSE_BODY_ERROR.format(response_body, response_status))

        if response_status < 200 or response_status >= 300:
            self._handle_api_error(
                response_status=response_status, response_body=response_body, response_json=response_json
            )

        return response_json

    def _handle_api_error(self, response_status: int, response_body: str, response_json: dict) -> None:
        """Handles API errors returned from the EasyPost API."""
        try:
            error = response_json["error"]
        except (KeyError, TypeError):
            raise JsonError(
                message=INVALID_RESPONSE_BODY_ERROR.format(response_status, response_body),
                http_status=response_status,
                http_body=response_body,
            )

        if 300 <= response_status < 400:
            raise RedirectError(message=error, http_status=response_status, http_body=response_body)

        error_type = STATUS_CODE_TO_ERROR_MAPPING.get(response_status, UnknownApiError)

        raise error_type(
            message=error.get("message", ""),
            http_status=response_status,
            http_body=response_body,
        )

    def request(
        self,
        klass: type,
        method: HttpMethod,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        root_key: Optional[str] = None,
        override_api_version: Optional[ApiVersion] = None,
    ) -> Any:
        """
        Make a request to the EasyPost API.

        :param klass: The class of the object to construct from the response JSON.
        :type klass: type
        :param method: The HTTP method to use.
        :type method: HttpMethod
        :param endpoint: The endpoint to hit.
        :type endpoint: str
        :param params: The parameters to send in the request.
        :type params: Optional[Dict[str, Any]]
        :param root_key: The root key of the response JSON.
        :type root_key: Optional[str]
        :param override_api_version: The API version to use.
        :type override_api_version: Optional[str]
        :return: An instance of `klass` constructed from the response JSON.
        :rtype: Any
        """
        # Prepare properties for the request
        params = params or {}
        params = self._objects_to_ids(param=params)  # TODO: Why passing a whole dict in here?

        api_version = override_api_version or self._api_version

        full_url = f"{self.api_base_url}/{endpoint}"

        headers = self._build_headers(api_version=api_version)

        # Run the request hook
        request_uuid = uuid.uuid4()
        request_timestamp = datetime.now(timezone.utc)
        self._request_hook(
            request_uuid=request_uuid,
            request_timestamp=request_timestamp,
            method=method,
            url=full_url,
            headers=headers,
            params=params,
        )

        # Make the request
        if self._request_engine == RequestEngine.URLFETCH:
            http_body, http_status, http_headers = self._request_with_urlfetch(
                method=method,
                abs_url=full_url,
                headers=headers,
                params=params,
            )
        elif self._request_engine == RequestEngine.REQUESTS:
            http_body, http_status, http_headers = self._request_with_requests(
                method=method,
                abs_url=full_url,
                headers=headers,
                params=params,
            )
        else:
            raise EasyPostError(INVALID_REQUEST_LIB_ERROR.format(self._request_engine, SUPPORT_EMAIL))

        # Run the response hook
        response_timestamp = datetime.now(timezone.utc)
        self._response_hook(
            request_uuid=request_uuid,
            request_timestamp=request_timestamp,
            response_timestamp=response_timestamp,
            method=method,
            url=full_url,
            headers=http_headers,
            response_body=http_body,
            response_status=http_status,
        )

        # Interpret the response
        valid_response_json = self._interpret_response(response_body=http_body, response_status=http_status)

        # Any HTTP error would have been handled at this point, so we can deserialize the response into an object now
        if root_key:
            try:
                valid_response_json = valid_response_json[root_key]
            except KeyError:
                raise JsonError(INVALID_RESPONSE_BODY_ERROR.format(http_status, http_body))

        return klass(**valid_response_json)
