import datetime
import json
import platform
import time
from enum import Enum
from json import JSONDecodeError
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)
from urllib.parse import urlencode

from easypost.constant import (
    SUPPORT_EMAIL,
    TIMEOUT,
)
from easypost.easypost_object import EasyPostObject
from easypost.error import Error


class RequestMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


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

    @staticmethod
    def form_encode_params(data: Dict, parent_keys: List[str] = None, parent_dict: Dict = None) -> Dict:
        """Form-encode a multi-layer dictionary to a one-layer dictionary."""
        result = parent_dict or {}
        keys = parent_keys or []

        for key, value in data.items():
            if isinstance(value, dict):
                keys.append(key)
                result = Requestor.form_encode_params(data=value, parent_keys=keys, parent_dict=result)
            else:
                dict_key = Requestor._build_dict_key(keys + [key])
                result[dict_key] = value
        return result

    @staticmethod
    def _build_dict_key(keys: List[str]) -> str:
        """Build a dict key from a list of keys.
        Example: [code, number] -> code[number]
        """
        result = keys[0]

        for key in keys[1:]:
            result += f"[{key}]"
        return result

    def request(
        self,
        method: RequestMethod,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        api_key_required: bool = True,
        beta: bool = False,
    ) -> Tuple[dict, Optional[str]]:
        """Make a request to the EasyPost API."""
        if params is None:
            params = {}
        http_body, http_status, my_api_key = self.request_raw(
            method=method,
            url=url,
            params=params,
            api_key_required=api_key_required,
            beta=beta,
        )
        response = self.interpret_response(http_body=http_body, http_status=http_status)
        return response, my_api_key

    def request_raw(
        self,
        method: RequestMethod,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        api_key_required: bool = True,
        beta: bool = False,
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

        if beta:
            abs_url = f"https://api.easypost.com/beta{url}"
        else:
            abs_url = f"{api_base}{url}"

        params = self._objects_to_ids(param=params or {})

        # Fallback values for the user-agent header
        user_agent = {
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
                    user_agent["os"] = val[0]
                    user_agent["os_version"] = val[2]
                    user_agent["os_arch"] = val[4]
                else:
                    user_agent[attr] = val  # type: ignore
            except Exception:  # nosec
                # If we fail to get OS info, do nothing as we already set fallbacks for these values
                pass

        user_agent = (
            f"EasyPost/v2 PythonClient/{VERSION} Python/{user_agent['python_version']}"  # type: ignore
            f" OS/{user_agent['os']} OSVersion/{user_agent['os_version']} OSArch/{user_agent['os_arch']}"
            f" Implementation/{user_agent['implementation']}"
        )

        headers = {
            "Authorization": "Bearer %s" % my_api_key,
            "User-Agent": user_agent,
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
        method: RequestMethod,
        abs_url: str,
        headers: Dict[str, Any],
        params: Dict[str, Any],
    ) -> Tuple[str, int]:
        """Make a request by using the `request` library."""
        if method in [RequestMethod.GET, RequestMethod.DELETE]:
            url_params = params
            body = None
        elif method in [RequestMethod.POST, RequestMethod.PATCH, RequestMethod.PUT]:
            url_params = None
            body = params
        else:
            # how did you reach here with an enum?
            raise Error(f"Bug discovered: invalid request method: {method}. Please report to {SUPPORT_EMAIL}.")

        if url_params and method not in [RequestMethod.GET, RequestMethod.DELETE]:
            raise Error("Only GET and DELETE requests support parameters.")

        try:
            result = requests_session.request(
                method=method.value,
                url=abs_url,
                params=url_params,
                headers=headers,
                json=body,
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
        method: RequestMethod,
        abs_url: str,
        headers: Dict[str, Any],
        params: Dict[str, Any],
    ) -> Tuple[str, int]:
        """Make a request by using the `urlfetch` library."""
        fetch_args = {"method": method.value, "headers": headers, "validate_certificate": False, "deadline": timeout}
        if method in [RequestMethod.GET, RequestMethod.DELETE]:
            # GET/DELETE requests use query params
            fetch_args["url"] = self.add_params_to_url(url=abs_url, params=params, method=method)
        elif method in [RequestMethod.POST, RequestMethod.PUT]:
            fetch_args["url"] = abs_url
            # POST/PUT requests use body params
            fetch_args["payload"] = json.dumps(params, default=self._utf8)
        else:
            # how did you reach here with an enum?
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

    def encode_url_params(self, params: Dict[str, Any], method: RequestMethod) -> Union[str, None]:
        """Encode params for a URL."""
        if method not in [RequestMethod.GET, RequestMethod.DELETE]:
            raise Error("Only GET and DELETE requests support parameters.")
        converted_params = []
        for key, value in sorted(params.items()):
            if value is None:
                continue  # Don't add Nones to the query
            elif isinstance(value, datetime.datetime):
                value = int(time.mktime(value.timetuple()))  # to UTC timestamp
            converted_params.append((key, value))
        return urlencode(query=converted_params)

    def add_params_to_url(self, url: str, params: Dict[str, Any], method: RequestMethod) -> str:
        """Add params to the URL."""
        if method not in [RequestMethod.GET, RequestMethod.DELETE]:
            raise Error("Only GET and DELETE requests support parameters.")
        encoded_params = self.encode_url_params(params=params, method=method)
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
