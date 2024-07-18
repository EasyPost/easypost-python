import enum
from typing import Optional

from easypost.easypost_object import EasyPostObject
from easypost.models.payment_method import PaymentMethod
from pydantic import Field


class PaymentMethodPriority(enum.Enum):
    Primary = "primary"
    Secondary = "secondary"


class PaymentMethodsSummary(EasyPostObject):
    primary: Optional[PaymentMethod] = Field(None, alias="primary_payment_method")
    secondary: Optional[PaymentMethod] = Field(None, alias="secondary_payment_method")
