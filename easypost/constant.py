# flake8: noqa
# Library version
VERSION = "10.1.0"
VERSION_INFO = [str(number) for number in VERSION.split(".")]

# Client defaults
API_BASE = "https://api.easypost.com"
API_VERSION = "v2"
AUTHOR = "EasyPost <oss@easypost.com>"
SUPPORT_EMAIL = "support@easypost.com"
TIMEOUT = 60

# Error messages
COMMUNICATION_ERROR = "Unexpected error communicating with EasyPost. If this problem persists please let us know at {}. Original error: {}"
INVALID_DELIVER_ACCURACY_ERROR = "Invalid delivery_accuracy value, must be one of: {}"
INVALID_PAYMENT_METHOD_ERROR = "The chosen payment method is not valid. Please try again."
INVALID_REQUEST_LIB_ERROR = "Bug discovered: invalid request_lib: {}. Please report to {}."
INVALID_REQUEST_METHOD_ERROR = "Bug discovered: invalid request method: {}. Please report to {}."
INVALID_REQUEST_PARAMETERS_ERROR = "Only GET and DELETE requests support parameters."
INVALID_REQUESTS_VERSION_ERROR = 'EasyPost requires an up to date requests library. Update requests via "pip install -U requests" or contact us at {}.'
INVALID_RESPONSE_BODY_ERROR = "Invalid response from API: ({}) {}"
INVALID_SIGNATURE_ERROR = "Webhook received does not contain an HMAC signature."
INVALID_WEBHOOK_VALIDATION_ERROR = "Webhook received did not originate from EasyPost or had a webhook secret mismatch."
MISSING_PARAMETER_ERROR = "Missing required parameter: {}"
NO_ATTRIBUTE_ERROR = "{} object has no attribute {}"
NO_BILLING_ERROR = "Billing has not been setup for this user. Please add a payment method."
NO_MORE_PAGES_ERROR = "There are no more pages to retrieve."
NO_RATES_ERROR = "No rates found."
NO_USER_FOUND = "No user found with the given id."
SEND_STRIPE_DETAILS_ERROR = "Could not send card details to Stripe, please try again later."
TIMEOUT_ERROR = "Request timed out."

# Internal constants (user's should not use these)
_TEST_FAILED_INTENTIONALLY_ERROR = "Test failed intentionally."
_CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_WORKFLOWS = [
    "FedexAccount",
    "FedexSmartpostAccount",
]
_CARRIER_ACCOUNT_TYPES_WITH_CUSTOM_OAUTH = [
    "AmazonShippingAccount",
    "UpsAccount",
    "UpsMailInnovationsAccount",
    "UpsSurepostAccount",
]
_FILTERS_KEY = "filters"
