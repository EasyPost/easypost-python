from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class TaxIdentifier(EasyPostObject):
    entity: Optional[str] = Field(None, alias="entity")
    issuing_country: Optional[str] = Field(None, alias="issuing_country")
    tax_id: Optional[str] = Field(None, alias="tax_id")
    tax_id_type: Optional[str] = Field(None, alias="tax_id_type")
