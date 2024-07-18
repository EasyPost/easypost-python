from typing import (
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from easypost.models.address import Address
from easypost.models.carrier_account import CarrierAccount
from easypost.models.customs_info import CustomsInfo
from easypost.models.fee import Fee
from easypost.models.form import Form
from easypost.models.message import Message
from easypost.models.options import Options
from easypost.models.parcel import Parcel
from easypost.models.postage_label import PostageLabel
from easypost.models.rate import Rate
from easypost.models.scan_form import ScanForm
from easypost.models.tax_identifier import TaxIdentifier
from easypost.models.tracker import Tracker
from easypost.util import get_lowest_object_rate
from pydantic import Field


class Shipment(EasyPostObject):
    batch_id: Optional[str] = Field(None, alias="batch_id")
    batch_message: Optional[str] = Field(None, alias="batch_message")
    batch_status: Optional[str] = Field(None, alias="batch_status")
    buyer_address: Optional[Address] = Field(None, alias="buyer_address")
    carrier_accounts: Optional[List[CarrierAccount]] = Field(None, alias="carrier_accounts")
    customs_info: Optional[CustomsInfo] = Field(None, alias="customs_info")
    fees: Optional[List[Fee]] = Field(None, alias="fees")
    forms: Optional[List[Form]] = Field(None, alias="forms")
    from_address: Optional[Address] = Field(None, alias="from_address")
    insurance: Optional[str] = Field(None, alias="insurance")
    is_return: Optional[bool] = Field(None, alias="is_return")
    messages: Optional[List[Message]] = Field(None, alias="messages")
    options: Optional[Options] = Field(None, alias="options")
    order_id: Optional[str] = Field(None, alias="order_id")
    parcel: Optional[Parcel] = Field(None, alias="parcel")
    postage_label: Optional[PostageLabel] = Field(None, alias="postage_label")
    rates: Optional[List[Rate]] = Field(None, alias="rates")
    reference: Optional[str] = Field(None, alias="reference")
    refund_status: Optional[str] = Field(None, alias="refund_status")
    return_address: Optional[Address] = Field(None, alias="return_address")
    scan_form: Optional[ScanForm] = Field(None, alias="scan_form")
    selected_rate: Optional[Rate] = Field(None, alias="selected_rate")
    service: Optional[str] = Field(None, alias="service")
    status: Optional[str] = Field(None, alias="status")
    tax_identifiers: Optional[List[TaxIdentifier]] = Field(None, alias="tax_identifiers")
    to_address: Optional[Address] = Field(None, alias="to_address")
    tracker: Optional[Tracker] = Field(None, alias="tracker")
    tracking_code: Optional[str] = Field(None, alias="tracking_code")
    usps_zone: Optional[str] = Field(None, alias="usps_zone")

    def lowest_rate(self, carriers: Optional[List[str]] = None, services: Optional[List[str]] = None) -> Rate:
        """Get the lowest rate of this shipment."""
        lowest_rate = get_lowest_object_rate(self, carriers, services)

        return lowest_rate


class ShipmentCollection(PaginatedCollection):
    shipments: List[Shipment] = Field([], alias="shipments")
