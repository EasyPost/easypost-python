import hashlib
import hmac
import json
import unicodedata
from typing import (
    Any,
    Optional,
    Union,
)

from easypost.constant import (
    INVALID_DELIVER_ACCURACY_ERROR,
    INVALID_SIGNATURE_ERROR,
    INVALID_WEBHOOK_VALIDATION_ERROR,
    NO_RATES_ERROR,
)
from easypost.easypost_object import (
    EasyPostObject,
    convert_to_easypost_object,
)
from easypost.errors import (
    FilteringError,
    InvalidParameterError,
    SignatureVerificationError,
)
from easypost.models.rate import Rate


def get_lowest_object_rate(
    easypost_object: Union[EasyPostObject, dict[str, Any]],
    carriers: Optional[list[str]] = None,
    services: Optional[list[str]] = None,
    rates_key: str = "rates",
) -> Rate:
    """Gets the lowest rate of an EasyPost object such as a Shipment, Order, or Pickup."""
    carriers = carriers or []
    services = services or []
    lowest_rate = None

    carriers = [carrier.lower() for carrier in carriers]
    services = [service.lower() for service in services]

    for rate in easypost_object.get(rates_key, []):
        if (carriers and rate.carrier.lower() not in carriers) or (services and rate.service.lower() not in services):
            continue

        if lowest_rate is None or float(rate.rate) < float(lowest_rate.rate):
            lowest_rate = rate

    if lowest_rate is None:
        raise FilteringError(message=NO_RATES_ERROR)

    return lowest_rate


def get_lowest_smart_rate(smart_rates: list[Rate], delivery_days: int, delivery_accuracy: str) -> Rate:
    """Get the lowest SmartRate from a list of SmartRates."""
    valid_delivery_accuracy_values = {
        "percentile_50",
        "percentile_75",
        "percentile_85",
        "percentile_90",
        "percentile_95",
        "percentile_97",
        "percentile_99",
    }
    lowest_smart_rate = None

    if delivery_accuracy.lower() not in valid_delivery_accuracy_values:
        raise InvalidParameterError(message=INVALID_DELIVER_ACCURACY_ERROR.format(valid_delivery_accuracy_values))

    for rate in smart_rates:
        if rate["time_in_transit"][delivery_accuracy] > delivery_days:
            continue
        elif lowest_smart_rate is None or float(rate["rate"]) < float(lowest_smart_rate["rate"]):
            lowest_smart_rate = rate

    if lowest_smart_rate is None:
        raise FilteringError(message=NO_RATES_ERROR)

    return lowest_smart_rate


def get_lowest_stateless_rate(
    stateless_rates: list[dict[str, Any]],
    carriers: Optional[list[str]] = None,
    services: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Get the lowest stateless rate."""
    carriers = carriers or []
    services = services or []
    lowest_rate = None

    carriers = [carrier.lower() for carrier in carriers]
    services = [service.lower() for service in services]

    for rate in stateless_rates:
        if (carriers and rate["carrier"].lower() not in carriers) or (
            services and rate["service"].lower() not in services
        ):
            continue

        if lowest_rate is None or float(rate["rate"]) < float(lowest_rate["rate"]):
            lowest_rate = rate

    if lowest_rate is None:
        raise FilteringError(message=NO_RATES_ERROR)

    return lowest_rate


def receive_event(raw_input: str):
    """Receives a raw Webhook event and converts it to JSON."""
    return convert_to_easypost_object(response=json.loads(raw_input))


def validate_webhook(event_body: bytes, headers: dict[str, Any], webhook_secret: str) -> dict[str, Any]:
    """Validate a webhook by comparing the HMAC signature header sent from EasyPost to your shared secret.
    If the signatures do not match, an error will be raised signifying the webhook either did not originate
    from EasyPost or the secrets do not match. If the signatures do match, the `event_body` will be returned
    as JSON.
    """
    easypost_hmac_signature = headers.get("X-Hmac-Signature")

    if easypost_hmac_signature:
        normalized_secret = unicodedata.normalize("NFKD", webhook_secret)
        encoded_secret = bytes(normalized_secret, "utf8")

        expected_signature = hmac.new(
            key=encoded_secret,
            msg=event_body,
            digestmod=hashlib.sha256,
        )

        digest = "hmac-sha256-hex=" + expected_signature.hexdigest()

        if hmac.compare_digest(digest, easypost_hmac_signature):
            webhook_body = json.loads(event_body)
        else:
            raise SignatureVerificationError(message=INVALID_WEBHOOK_VALIDATION_ERROR)
    else:
        raise SignatureVerificationError(message=INVALID_SIGNATURE_ERROR)

    return webhook_body
