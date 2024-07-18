from datetime import datetime
from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class PostageLabel(EasyPostObject):
    date_advance: Optional[int] = Field(None, alias="date_advance")
    integrated_form: Optional[str] = Field(None, alias="integrated_form")
    label_date: Optional[datetime] = Field(None, alias="label_date")
    label_epl2_url: Optional[str] = Field(None, alias="label_epl2_url")
    label_file: Optional[str] = Field(None, alias="label_file")
    label_file_type: Optional[str] = Field(None, alias="label_file_type")
    label_pdf_url: Optional[str] = Field(None, alias="label_pdf_url")
    label_resolution: Optional[int] = Field(None, alias="label_resolution")
    label_size: Optional[str] = Field(None, alias="label_size")
    label_type: Optional[str] = Field(None, alias="label_type")
    label_url: Optional[str] = Field(None, alias="label_url")
    label_zpl_url: Optional[str] = Field(None, alias="label_zpl_url")
