import os

from easypost.easypost_client import EasyPostClient


def test_api_key():
    """Tests setting and getting API keys from different client objects."""
    client1 = EasyPostClient(api_key="123")
    assert client1.api_key == "123"

    client2 = EasyPostClient(api_key="456")
    assert client2.api_key == "456"


def test_api_base():
    """Tests that we can override the API base of the client object."""
    client1 = EasyPostClient(api_key="123")
    assert client1.api_base == "https://api.easypost.com/v2"

    client2 = EasyPostClient(api_key="123", api_base="http://example.com")
    assert client2.api_base == "http://example.com"


def test_client_timeout():
    """Tests that we override the timeout of a client."""
    # TODO: Make an actual API call to ensure these get passed down to the request once the dust settles
    client = EasyPostClient(api_key=os.getenv("EASYPOST_TEST_API_KEY"))
    assert client.timeout == 60

    client = EasyPostClient(api_key=os.getenv("EASYPOST_TEST_API_KEY"), timeout=1)
    assert client.timeout == 1


# TODO: Add a test for no API key once that logic gets moved to the client
# TODO: Add a test for invalid property on a client once the dust settles
