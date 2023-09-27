import pytest
from easypost.models import ApiKey


@pytest.mark.vcr()
def test_all_api_keys(prod_client):
    """Tests that we can retrieve all API keys."""
    api_keys = prod_client.api_keys.all()

    assert all(isinstance(key, ApiKey) for key in api_keys.keys)
    for child in api_keys.children:
        assert all(isinstance(key, ApiKey) for key in child["keys"])


@pytest.mark.vcr()
def test_authenticated_user_api_keys(prod_client):
    """Tests that we can retrieve the authenticated user's API keys."""
    user = prod_client.user.retrieve_me()
    api_keys = prod_client.api_keys.retrieve_api_keys_for_user(user.id)

    assert all(isinstance(key, ApiKey) for key in api_keys)


@pytest.mark.vcr()
def test_child_user_api_keys(prod_client):
    """Tests that we can retrieve a child user's API keys as the parent."""
    user = prod_client.user.create(name="Test User")
    child_user = prod_client.user.retrieve(user.id)

    api_keys = prod_client.api_keys.retrieve_api_keys_for_user(child_user.id)

    assert all(isinstance(key, ApiKey) for key in api_keys)

    # Delete the user so we don't clutter up the test environment
    prod_client.user.delete(child_user.id)
