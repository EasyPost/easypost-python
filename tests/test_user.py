import pytest
from easypost.constant import (
    _FILTERS_KEY,
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.models import (
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
def test_user_update_brand(prod_client):
    user = prod_client.user.retrieve_me()

    color = "#123456"

    brand = prod_client.user.update_brand(user.id, color=color)

    assert isinstance(brand, Brand)
    assert str.startswith(brand.id, "brd_")
    assert brand.color == color


@pytest.mark.vcr()
def test_user_all_children(prod_client, page_size):
    children_data = prod_client.user.all_children(page_size=page_size)

    children_array = children_data["children"]
    assert len(children_array) <= page_size
    assert all(isinstance(child, User) for child in children_array)

    has_more = children_data["has_more"]
    assert isinstance(has_more, bool)


@pytest.mark.vcr()
def test_user_children_get_next_page(prod_client, page_size):
    try:
        first_page = prod_client.user.all_children(page_size=page_size)
        next_page = prod_client.user.get_next_page_of_children(children=first_page, page_size=page_size)

        first_id_of_first_page = first_page["children"][0].id
        first_id_of_second_page = next_page["children"][0].id

        assert first_id_of_first_page != first_id_of_second_page

        # Verify that the filters are being passed along for behind-the-scenes reference
        assert first_page[_FILTERS_KEY] == next_page[_FILTERS_KEY]
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(_TEST_FAILED_INTENTIONALLY_ERROR)
