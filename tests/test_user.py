import pytest
from easypost.models import (
    ApiKey,
    Brand,
    User,
)


@pytest.mark.vcr()
def test_user_create(prod_client):
    user = prod_client.user.create(name="Test User")

    assert isinstance(user, User)
    assert str.startswith(user.id, "user_")
    assert user.name == "Test User"

    # Delete the user so we don't clutter up the test environment
    prod_client.user.delete(user.id)


@pytest.mark.vcr()
def test_user_retrieve(prod_client):
    authenticated_user = prod_client.user.retrieve_me()

    user = prod_client.user.retrieve(authenticated_user["id"])

    assert isinstance(user, User)
    assert str.startswith(user.id, "user_")


@pytest.mark.vcr()
def test_user_retrieve_no_id(prod_client):
    """If no ID is specified when retrieving a user, we'll retrieve the authenticated user."""
    user = prod_client.user.retrieve()

    assert isinstance(user, User)
    assert str.startswith(user.id, "user_")


@pytest.mark.vcr()
def test_user_retrieve_me(prod_client):
    user = prod_client.user.retrieve_me()

    assert isinstance(user, User)
    assert str.startswith(user.id, "user_")


@pytest.mark.vcr()
def test_user_update(prod_client):
    user = prod_client.user.retrieve_me()

    test_name = "New Name"

    updated_user = prod_client.user.update(user.id, name=test_name)

    assert isinstance(updated_user, User)
    assert str.startswith(updated_user.id, "user_")
    assert updated_user.name == test_name


@pytest.mark.vcr()
def test_user_delete(prod_client):
    user = prod_client.user.create(name="Test User")

    # Nothing gets returned here, simply ensure no error gets raised
    prod_client.user.delete(user.id)


@pytest.mark.vcr()
def test_user_all_api_keys(prod_client):
    """Tests that we can retrieve all API keys."""
    api_keys = prod_client.user.all_api_keys()

    assert all(isinstance(key, ApiKey) for key in api_keys.keys)
    for child in api_keys.children:
        assert all(isinstance(key, ApiKey) for key in child["keys"])


@pytest.mark.vcr()
def test_authenticated_user_api_keys(prod_client):
    """Tests that we can retrieve the authenticated user's API keys."""
    user = prod_client.user.retrieve_me()
    api_keys = prod_client.user.api_keys(user.id)

    assert all(isinstance(key, ApiKey) for key in api_keys)


@pytest.mark.vcr()
def test_child_user_api_keys(prod_client):
    """Tests that we can retrieve a child user's API keys as the parent."""
    user = prod_client.user.create(name="Test User")
    child_user = prod_client.user.retrieve(user.id)

    api_keys = prod_client.user.api_keys(child_user.id)

    assert all(isinstance(key, ApiKey) for key in api_keys)

    # Delete the user so we don't clutter up the test environment
    prod_client.user.delete(child_user.id)


@pytest.mark.vcr()
def test_user_update_brand(prod_client):
    user = prod_client.user.retrieve_me()

    color = "#123456"

    brand = prod_client.user.update_brand(user.id, color=color)

    assert isinstance(brand, Brand)
    assert str.startswith(brand.id, "brd_")
    assert brand.color == color
