import datetime
import json
import platform
import ssl
import time
from json import JSONDecodeError
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Union,
)
from urllib.parse import urlencode

from easypost.constant import (
    SUPPORT_EMAIL,
    TIMEOUT,
    USER_AGENT,
)
from easypost.easypost_object import EasyPostObject
from easypost.error import Error


class Requestor:
    def __init__(self, local_api_key: Optional[str] = None):
        self._api_key = local_api_key

    @classmethod
    def _objects_to_ids(cls, param: Dict[str, Any]) -> Dict[str, Any]:
        """If providing an object as a parameter to another object,
        only pass along the ID so the API will use the object reference correctly."""
        if isinstance(param, EasyPostObject):
            return {"id": param.id}
        elif isinstance(param, dict):
            data = {}
            for (k, v) in param.items():
                if isinstance(v, list):
                    data[k] = [cls._objects_to_ids(item) for item in v]  # type: ignore
                else:
                    data[k] = cls._objects_to_ids(v)  # type: ignore
            return data
        else:
            return param

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        api_key_required: bool = True,
    ) -> Tuple[dict, Optional[str]]:
        """Make a request to the EasyPost API."""
        if params is None:
            params = {}
        http_body, http_status, my_api_key = self.request_raw(
            method=method, url=url, params=params, api_key_required=api_key_required
        )
        response = self.interpret_response(http_body=http_body, http_status=http_status)
        return response, my_api_key

    def request_raw(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        api_key_required: bool = True,
    ) -> Tuple[str, int, Optional[str]]:
        """Internal logic required to make a request to the EasyPost API."""
        # Importing here to avoid circular imports
        from easypost import (
            VERSION,
            api_base,
            api_key,
        )

        my_api_key = self._api_key or api_key

        if api_key_required and my_api_key is None:
            raise Error(
                "No API key provided. Set an API key via \"easypost.api_key = 'APIKEY'. "
                "Your API keys can be found in your EasyPost dashboard, or you can email us "
                f"at {SUPPORT_EMAIL} for assistance."
            )

        abs_url = "%s%s" % (api_base, url or "")
        params = self._objects_to_ids(param=params or {})

        ua = {
            "client_version": VERSION,
            "lang": "python",
            "publisher": "easypost",
            "request_lib": request_lib,
        }
        for attr, func in (
            ("lang_version", platform.python_version),
            ("platform", platform.platform),
            ("uname", lambda: " ".join(platform.uname())),
            ("implementation", platform.python_implementation),
        ):
            try:
                val = func()  # type: ignore
            except Exception as e:
                val = "!! %s" % e
            ua[attr] = val

        if hasattr(ssl, "OPENSSL_VERSION"):
            ua["openssl_version"] = ssl.OPENSSL_VERSION

        headers = {
            "X-Client-User-Agent": json.dumps(ua),
            "User-Agent": USER_AGENT,
            "Authorization": "Bearer %s" % my_api_key,
        }

        if request_lib == "urlfetch":
            http_body, http_status = self.urlfetch_request(
                method=method, abs_url=abs_url, headers=headers, params=params
            )
        elif request_lib == "requests":
            http_body, http_status = self.requests_request(
                method=method, abs_url=abs_url, headers=headers, params=params
            )
        else:
            raise Error(f"Bug discovered: invalid request_lib: {request_lib}. Please report to {SUPPORT_EMAIL}.")

        return http_body, http_status, my_api_key

    def interpret_response(self, http_body: str, http_status: int) -> Dict[str, Any]:
        """Interpret the response body we receive from the API."""
        if http_status == 204:
            # HTTP 204 does not have any response body and we can just return here
            return {}
        try:
            response = json.loads(http_body)
        except JSONDecodeError:
            raise Exception(
                f"Unable to parse response body from API: {http_body}\nHTTP response code was: {http_status}"
            )
        if not (200 <= http_status < 300):
            self.handle_api_error(http_status=http_status, http_body=http_body, response=response)
        return response

    def requests_request(
        self,
        method: str,
        abs_url: str,
        headers: Dict[str, Any],
        params: Dict[str, Any],
    ) -> Tuple[str, int]:
        """Make a request by using the `request` library."""
        method = method.lower()
        if method == "get" or method == "delete":
            url_params = params
            json = None
        elif method == "post" or method == "put":
            json = params
            url_params = None
        else:
            raise Error(f"Bug discovered: invalid request method: {method}. Please report to {SUPPORT_EMAIL}.")

        try:
            result = requests_session.request(
                method,
                abs_url,
                params=url_params,
                headers=headers,
                json=json,
                timeout=timeout,
                verify=True,
            )
            http_body = result.text
            http_status = result.status_code
        except Exception as e:
            raise Error(
                "Unexpected error communicating with EasyPost. If this "
                f"problem persists please let us know at {SUPPORT_EMAIL}.",
                original_exception=e,
            )
        return http_body, http_status

    def urlfetch_request(
        self,
        method: str,
        abs_url: str,
        headers: Dict[str, Any],
        params: Dict[str, Any],
    ) -> Tuple[str, int]:
        """Make a request by using the `urlfetch` library."""
        fetch_args = {"method": method, "headers": headers, "validate_certificate": False, "deadline": timeout}
        if method == "get" or method == "delete":
            fetch_args["url"] = self.add_params_to_url(url=abs_url, params=params)
        elif method == "post" or method == "put":
            fetch_args["url"] = abs_url
            fetch_args["payload"] = json.dumps(params, default=self._utf8)
        else:
            raise Error(f"Bug discovered: invalid request method: {method}. Please report to {SUPPORT_EMAIL}.")

        try:
            from google.appengine.api import urlfetch  # type: ignore

            result = urlfetch.fetch(**fetch_args)  # type: ignore
        except Exception as e:
            raise Error(
                "Unexpected error communicating with EasyPost. "
                f"If this problem persists, let us know at {SUPPORT_EMAIL}.",
                original_exception=e,
            )

        return result.content, result.status_code

    def handle_api_error(self, http_status: int, http_body: str, response: Dict[str, Any]) -> None:
        """Handles API errors returned from EasyPost."""
        try:
            error = response["error"]
        except (KeyError, TypeError):
            raise Error("Invalid response from API: (%d) %r " % (http_status, http_body), http_status, http_body)

        try:
            raise Error(message=error.get("message", ""), http_status=http_status, http_body=http_body)
        except AttributeError:
            raise Error(message=error, http_status=http_status, http_body=http_body)

    def _utf8(self, value: Union[str, bytes]) -> str:
        # Python3's str(bytestring) returns "b'bytestring'" so we use .decode instead
        if isinstance(value, bytes):
            return value.decode(encoding="utf-8")
        return value

    def encode_url_params(self, params: Dict[str, Any]) -> Union[str, None]:
        """Encode params for a URL."""
        converted_params = []
        for key, value in sorted(params.items()):
            if value is None:
                continue  # Don't add Nones to the query
            elif isinstance(value, datetime.datetime):
                value = int(time.mktime(value.timetuple()))  # to UTC timestamp
            converted_params.append((key, value))
        return urlencode(query=converted_params)

    def add_params_to_url(self, url: str, params: Dict[str, Any]) -> str:
        """Add params to the URL."""
        encoded_params = self.encode_url_params(params=params)
        if encoded_params:
            return "%s?%s" % (url, encoded_params)
        return url


# use urlfetch as request_lib on google app engine, otherwise use requests
request_lib = None
try:
    from google.appengine.api import urlfetch

    request_lib = "urlfetch"
    # use the GAE application-wide "deadline" (or its default)
    timeout = urlfetch.get_default_fetch_deadline() or TIMEOUT
except ImportError:
    timeout = TIMEOUT
    try:
        import requests

        request_lib = "requests"
        requests_session = requests.Session()
        requests_http_adapter = requests.adapters.HTTPAdapter(max_retries=3)
        requests_session.mount(prefix="https://api.easypost.com", adapter=requests_http_adapter)
    except Exception:
        raise ImportError(
            "EasyPost requires an up to date requests library. "
            'Update requests via "pip install -U requests" or '
            f"contact us at {SUPPORT_EMAIL}."
        )

    try:
        version = requests.__version__
        major, minor, patch = [int(i) for i in version.split(".")]
    except Exception:
        raise ImportError(
            "EasyPost requires an up to date requests library. "
            'Update requests via "pip install -U requests" or contact '
            f"us at {SUPPORT_EMAIL}."
        )
    else:
        if major < 1:
            raise ImportError(
                "EasyPost requires an up to date requests library. Update "
                'requests via "pip install -U requests" or contact us '
                f"at {SUPPORT_EMAIL}."
            )
