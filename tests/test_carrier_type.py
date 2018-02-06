# Unit tests related to 'CarrierType' (https://www.easypost.com/docs/api#carrier-types).

import easypost


def test_carrier_types(prod_api_key):
    carriers = easypost.CarrierAccount.types()

    assert len(carriers) > 0

    for carrier in carriers:
        if carrier.type == 'AustraliaPostAccount':
            assert hasattr(carrier.fields.credentials, 'api_key')
            assert hasattr(carrier.fields.credentials, 'api_secret')
            assert hasattr(carrier.fields.credentials, 'account_number')
            assert hasattr(carrier.fields.credentials, 'print_as_you_go')

            assert isinstance(carrier.fields.credentials.api_key, easypost.EasyPostObject)
            assert isinstance(carrier.fields.credentials.api_secret, easypost.EasyPostObject)
            assert isinstance(carrier.fields.credentials.account_number, easypost.EasyPostObject)
            assert isinstance(carrier.fields.credentials.print_as_you_go, easypost.EasyPostObject)
