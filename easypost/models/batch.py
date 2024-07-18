from typing import (
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    PaginatedCollection,
)
from easypost.models.batch_shipment import BatchShipment
from easypost.models.scan_form import ScanForm
from pydantic import Field


class Batch(EasyPostObject):
    error: Optional[str] = Field(None, alias="error")
    label_url: Optional[str] = Field(None, alias="label_url")
    message: Optional[str] = Field(None, alias="message")
    num_shipments: Optional[int] = Field(None, alias="num_shipments")
    reference: Optional[str] = Field(None, alias="reference")
    scan_form: Optional[ScanForm] = Field(None, alias="scan_form")
    shipments: Optional[List[BatchShipment]] = Field(None, alias="shipments")
    state: Optional[str] = Field(None, alias="state")
    status: Optional[Dict[str, int]] = Field(None, alias="status")


class BatchCollection(PaginatedCollection):
    batches: List[Batch] = Field([], alias="batches")
