import hashlib
import hmac
import json
import unicodedata
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from easypost.error import Error
from easypost.models import (
    Address,
    ApiKey,
    Batch,
    Brand,
    CarrierAccount,
    CustomsInfo,
    CustomsItem,
    EndShipper,
    Event,
    Insurance,
    Order,
    Parcel,
    Payload,
    Pickup,
    PickupRate,
    PostageLabel,
    Rate,
    Refund,
    Report,
    ScanForm,
    Shipment,
    Tracker,
    User,
    Webhook,
)


EASYPOST_OBJECT_ID_PREFIX_TO_CLASS_NAME_MAP: Dict[str, Any] = {
    "adr": Address,
    "ak": ApiKey,
    "batch": Batch,
    "brd": Brand,
    "ca": CarrierAccount,
    "cfrep": Report,
    "cstinfo": CustomsInfo,
    "cstitem": CustomsItem,
    "es": EndShipper,
    "evt": Event,
    "hook": Webhook,
    "ins": Insurance,
    "order": Order,
    "payload": Payload,
    "pickup": Pickup,
    "pickuprate": PickupRate,
    "pl": PostageLabel,
    "plrep": Report,
    "prcl": Parcel,
    "rate": Rate,
    "refrep": Report,
    "rfnd": Refund,
    "sf": ScanForm,
    "shp": Shipment,
    "shpinvrep": Report,
    "shprep": Report,
    "trk": Tracker,
    "trkrep": Report,
    "user": User,
}

OBJECT_CLASS_NAME_OVERRIDES: Dict[str, Any] = {
    "CashFlowReport": Report,
    "PaymentLogReport": Report,
    "RefundReport": Report,
    "ShipmentInvoiceReport": Report,
    "ShipmentReport": Report,
    "TrackerReport": Report,
}


def convert_to_easypost_object(
    response: Dict[str, Any],
    api_key: Optional[str] = None,
    parent: object = None,
    name: Optional[str] = None,
):
    """Convert a response to an EasyPost object."""
    if isinstance(response, list):
        return [convert_to_easypost_object(response=item, api_key=api_key, parent=parent) for item in response]
    elif isinstance(response, dict):
        response = response.copy()
        object_type_str = response.get("object", EasyPostObject)
        class_object = OBJECT_CLASS_NAME_OVERRIDES.get(object_type_str, object_type_str)
        object_id = response.get("id", None)

        if object_id is not None:
            # If an object ID is present, use it to find the class type instead.
            object_id_prefix = object_id.split("_")[0]
            class_object = EASYPOST_OBJECT_ID_PREFIX_TO_CLASS_NAME_MAP.get(object_id_prefix, EasyPostObject)

        obj = class_object.construct_from(values=response, api_key=api_key, parent=parent, name=name)

        return obj
    else:
        return response


def get_lowest_object_rate(
    easypost_object: EasyPostObject,
    carriers: Optional[List[str]] = None,
    services: Optional[List[str]] = None,
    rates_key: str = "rates",
):
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
        raise Error(message="No rates found.")

    return lowest_rate


def get_lowest_smart_rate(smart_rates, delivery_days: int, delivery_accuracy: str) -> Rate:
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
        raise Error(message=f"Invalid delivery_accuracy value, must be one of: {valid_delivery_accuracy_values}")

    for rate in smart_rates:
        if rate["time_in_transit"][delivery_accuracy] > delivery_days:
            continue
        elif lowest_smart_rate is None or float(rate["rate"]) < float(lowest_smart_rate["rate"]):
            lowest_smart_rate = rate

    if lowest_smart_rate is None:
        raise Error(message="No rates found.")

    return lowest_smart_rate


def get_lowest_stateless_rate(
    stateless_rates: List[Dict[str, Any]], carriers: Optional[List[str]] = None, services: Optional[List[str]] = None
) -> Dict[str, Any]:
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

        if lowest_rate is None or float(rate.rate) < float(lowest_rate.rate):
            lowest_rate = rate

    if lowest_rate is None:
        raise Error(message="No rates found.")

    return lowest_rate


def receive_event(raw_input: str) -> Event:
    """Receives a raw Webhook event and converts it to JSON."""
    # TODO: Remove api_key
    return convert_to_easypost_object(response=json.loads(raw_input), api_key=None)


def validate_webhook(event_body: bytes, headers: Dict[str, Any], webhook_secret: str) -> Dict[str, Any]:
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
            raise Error(message="Webhook received did not originate from EasyPost or had a webhook secret mismatch.")
    else:
        raise Error(message="Webhook received does not contain an HMAC signature.")

    return webhook_body
