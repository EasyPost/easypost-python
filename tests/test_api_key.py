import os

import pytest

from easypost import EasyPostClient
from easypost.models import ApiKey


@pytest.mark.vcr()
def test_api_key_retrieve_authenticated_user(prod_client):
    """Tests that we can retrieve the authenticated user's API keys."""
    user = prod_client.user.retrieve_me()
    api_keys = prod_client.api_keys.retrieve_api_keys_for_user(user.id)

    assert all(isinstance(key, ApiKey) for key in api_keys)


@pytest.mark.vcr()
def test_api_key_retrieve_child_user(prod_client):
    """Tests that we can retrieve a child user's API keys as the parent."""
    user = prod_client.user.create(name="Test User")
    child_user = prod_client.user.retrieve(user.id)

    api_keys = prod_client.api_keys.retrieve_api_keys_for_user(child_user.id)

    assert all(isinstance(key, ApiKey) for key in api_keys)

    # Delete the user so we don't clutter up the test environment
    prod_client.user.delete(child_user.id)


@pytest.mark.vcr()
def test_api_key_all(prod_client):
    """Tests that we can retrieve all API keys."""
    api_keys = prod_client.api_keys.all()

    assert all(isinstance(key, ApiKey) for key in api_keys.keys)
    for child in api_keys.children:
        assert all(isinstance(key, ApiKey) for key in child["keys"])


@pytest.mark.vcr()
def test_api_key_lifecycle():
    """Tests creating an API key for a child user."""
    # Create an API key
    referral_client = EasyPostClient(os.getenv("REFERRAL_CUSTOMER_PROD_API_KEY"))
    api_key = referral_client.api_keys.create("production")
    assert isinstance(api_key, ApiKey)
    assert api_key.id.startswith("ak_")
    assert api_key.mode == "production"

    # Disable the API key
    api_key = referral_client.api_keys.disable(api_key.id)
    assert api_key.active is False

    # Enable the API key
    api_key = referral_client.api_keys.enable(api_key.id)
    assert api_key.active is True

    # Delete the API key
    referral_client.api_keys.delete(api_key.id)
