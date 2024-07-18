from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Brand(EasyPostObject):
    ad: Optional[str] = Field(None, alias="ad")
    ad_href: Optional[str] = Field(None, alias="ad_href")
    background_color: Optional[str] = Field(None, alias="background_color")
    color: Optional[str] = Field(None, alias="color")
    logo: Optional[str] = Field(None, alias="logo")
    logo_href: Optional[str] = Field(None, alias="logo_href")
    name: Optional[str] = Field(None, alias="name")
    theme: Optional[str] = Field(None, alias="theme")
    user_id: Optional[str] = Field(None, alias="user_id")
