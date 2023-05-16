import json
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    convert_to_easypost_object,
)
from easypost.error import Error
from easypost.models.event import Event
from easypost.models.rate import Rate


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
