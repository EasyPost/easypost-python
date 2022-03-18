import pytest

import easypost


@pytest.mark.vcr()
def test_error():
    try:
        _ = easypost.Shipment.create()
    except easypost.Error as error:
        assert error.http_status == 422
        assert (
            error.http_body == '{"error":{"code":"SHIPMENT.INVALID_PARAMS","message":"Unable to create '
            'shipment, one or more parameters were invalid.","errors":[{"to_address":"Required and missing."},'
            '{"from_address":"Required and missing."}]}}'
        )
        assert error.message == "Unable to create shipment, one or more parameters were invalid."
