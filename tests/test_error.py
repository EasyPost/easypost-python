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


def test_error_no_json():
    """Tests if we don't have valid JSON that we don't set the JSON body of an error."""
    error = easypost.Error(http_body="bad json")

    assert error.json_body is None


def test_error_list_message():
    """Tests that we concatenate error messages that are a list (they should be a string from the
    API but aren't always so we protect against that here).
    """
    error = easypost.Error(message=["Error1", "Error2"])

    assert error.message == "Error1, Error2"


def test_error_dict_message():
    """Tests that we concatenate error messages that are a dict (they should be a string from the
    API but aren't always so we protect against that here).
    """
    message_data = {"errors": ["Bad format 1", "Bad format 2"]}

    error = easypost.Error(message=message_data)

    assert error.message == "Bad format 1, Bad format 2"


def test_error_bad_format_message():
    """Tests that we concatenate error messages that has really bad format
    (they should be a string from the API but aren't always so we protect against that here).
    """
    message_data = {
        "errors": ["Bad format 1", "Bad format 2"],
        "bad_data": [
            {"first_message": "Bad format 3", "second_message": "Bad format 4", "thrid_message": "Bad format 5"}
        ],
    }

    error = easypost.Error(message=message_data)

    assert error.message == "Bad format 1, Bad format 2, Bad format 3, Bad format 4, Bad format 5"
