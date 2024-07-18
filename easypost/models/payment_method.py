import enum
from typing import Optional

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class PaymentMethodType(enum.Enum):
    CreditCard = "CreditCard"
    BankAccount = "BankAccount"


class PaymentMethod(EasyPostObject):
    bank_name: Optional[str] = Field(None, alias="bank_name")
    brand: Optional[str] = Field(None, alias="brand")
    country: Optional[str] = Field(None, alias="country")
    disabled_at: Optional[str] = Field(None, alias="disabled_at")
    expiration_month: Optional[int] = Field(None, alias="exp_month")
    expiration_year: Optional[int] = Field(None, alias="exp_year")
    last4: Optional[str] = Field(None, alias="last4")
    name: Optional[str] = Field(None, alias="name")
    verified: Optional[bool] = Field(None, alias="verified")

    @property
    def type(self):
        _object = self.object

        if _object == "CreditCard":
            return PaymentMethodType.CreditCard
        elif _object == "BankAccount":
            return PaymentMethodType.BankAccount
        else:
            return None

    @property
    def endpoint(self):
        _type = self.type
        if _type == PaymentMethodType.CreditCard:
            return "credit_cards"
        elif _type == PaymentMethodType.BankAccount:
            return "bank_accounts"
        else:
            return None
