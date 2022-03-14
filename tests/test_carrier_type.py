# Unit tests related to 'CarrierType' (https://www.easypost.com/docs/api#carrier-types).

import pytest

import easypost
from easypost.easypost_object import EasyPostObject


@pytest.mark.vcr()
def test_carrier_types(prod_api_key):
    carriers = easypost.CarrierAccount.types()

    assert len(carriers) > 0

    for carrier in carriers:
        if carrier.type == "AustraliaPostAccount":
            assert hasattr(carrier.fields.credentials, "api_key")
            assert hasattr(carrier.fields.credentials, "api_secret")
            assert hasattr(carrier.fields.credentials, "account_number")
            assert hasattr(carrier.fields.credentials, "print_as_you_go")

            assert isinstance(carrier.fields.credentials.api_key, EasyPostObject)
            assert isinstance(carrier.fields.credentials.api_secret, EasyPostObject)
            assert isinstance(carrier.fields.credentials.account_number, EasyPostObject)
            assert isinstance(carrier.fields.credentials.print_as_you_go, EasyPostObject)
