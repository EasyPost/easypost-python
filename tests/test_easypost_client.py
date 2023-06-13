import os
from unittest.mock import patch

import pytest
import requests
from easypost.easypost_client import EasyPostClient
from easypost.errors import TimeoutError


def test_api_key():
    """Tests setting and getting API keys from different client objects."""
    client1 = EasyPostClient(api_key="123")
    assert client1.api_key == "123"

    client2 = EasyPostClient(api_key="456")
    assert client2.api_key == "456"


def test_no_api_key():
    """Tests that we raise an error when no API key is passed to the client."""
    with pytest.raises(TypeError) as error:
        EasyPostClient()

    assert "missing 1 required positional argument: 'api_key'" in str(error.value)


def test_invalid_client_property():
    """Tests that we throw an error when attempting to use an invalid property of a client."""
    with pytest.raises(AttributeError) as error:
        EasyPostClient("123").invalid_property()

    assert str(error.value) == "'EasyPostClient' object has no attribute 'invalid_property'"


def test_api_base():
    """Tests that we can override the API base of the client object."""
    client1 = EasyPostClient(api_key="123")
    assert client1.api_base == "https://api.easypost.com/v2"

    client2 = EasyPostClient(api_key="123", api_base="http://example.com")
    assert client2.api_base == "http://example.com"


@patch("requests.Session")
def test_client_timeout(mock_session, basic_shipment):
    """Tests that the timeout gets used properly in requests when set."""
    mock_session().request.side_effect = requests.exceptions.Timeout()
    client = EasyPostClient(api_key=os.getenv("EASYPOST_TEST_API_KEY"), timeout=0.1)

    try:
        client.shipment.create(**basic_shipment)
        assert False
    except TimeoutError as error:
        assert error.message == "Request timed out."
