import pytest
from easypost.errors.api.api_error import ApiError


@pytest.mark.vcr()
def test_error(test_client):
    """Tests that we assign properties of an error correctly."""
    try:
        # Create a purposefully empty shipment so we can work with the returned error
        _ = test_client.shipment.create()
    except ApiError as error:
        assert error.http_status == 422
        assert error.code == "PARAMETER.REQUIRED"
        assert error.message == "Missing required parameter."
        assert error.errors[0] == {"field": "shipment", "message": "cannot be blank"}
        assert (
            error.http_body
            == '{"error": {"code": "PARAMETER.REQUIRED", "message": "Missing required parameter.", "errors": [{"field": "shipment", "message": "cannot be blank"}]}}'  # noqa
        )


def test_error_no_json():
    """Tests if we don't have valid JSON that we don't set the JSON body of an error."""
    error = ApiError(message="", http_body="bad json")

    assert error.json_body is None


def test_error_list_message():
    """Tests that we concatenate error messages that are a list (they should be a string from the
    API but aren't always so we protect against that here).
    """
    error = ApiError(message=["Error1", "Error2"])

    assert error.message == "Error1, Error2"


def test_error_dict_message():
    """Tests that we concatenate error messages that are a dict.

    Error messages from the API should be a string but aren't always, we protect against that here.
    """
    message_data = {"errors": ["Bad format 1", "Bad format 2"]}

    error = ApiError(message=message_data)

    assert error.message == "Bad format 1, Bad format 2"


def test_error_bad_format_message():
    """Tests that we concatenate error messages that has an invalid format.

    Error messages from the API should be a string but aren't always, we protect against that here.
    """
    message_data = {
        "errors": ["Bad format 1", "Bad format 2"],
        "bad_data": [
            {"first_message": "Bad format 3", "second_message": "Bad format 4", "thrid_message": "Bad format 5"}
        ],
    }

    error = ApiError(message=message_data)

    assert error.message == "Bad format 1, Bad format 2, Bad format 3, Bad format 4, Bad format 5"
