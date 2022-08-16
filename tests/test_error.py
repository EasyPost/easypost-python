import pytest

import easypost


@pytest.mark.vcr()
def test_error():
    try:
        _ = easypost.Shipment.create()
    except easypost.Error as error:
        assert error.http_status == 422
        assert (
            error.http_body
            == '{"error": {"code": "PARAMETER.REQUIRED", "message": "Missing required parameter.", "errors": [{"field": "shipment", "message": "cannot be blank"}]}}'  # noqa
        )
        assert error.message == "Missing required parameter."
