from typing import List

from easypost.easypost_object import EasyPostObject
from easypost.error import Error


def get_lowest_object_rate(
    easypost_object: EasyPostObject,
    carriers: List[str] = None,
    services: List[str] = None,
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
