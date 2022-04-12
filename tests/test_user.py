import pytest

import easypost


@pytest.mark.vcr()
@pytest.mark.skip(reason="This endpoint returns the child user keys in plain text, do not run this test.")
def test_user_create(prod_api_key):
    user = easypost.User.create(name="Test User")

    assert isinstance(user, easypost.User)
    assert str.startswith(user.id, "user_")
    assert user.name == "Test User"


@pytest.mark.vcr()
def test_user_retrieve(prod_api_key):
    authenticated_user = easypost.User.retrieve_me()

    user = easypost.User.retrieve(authenticated_user["children"][0]["id"])

    assert isinstance(user, easypost.User)
    assert str.startswith(user.id, "user_")


@pytest.mark.vcr()
def test_user_retrieve_me(prod_api_key):
    user = easypost.User.retrieve_me()

    assert isinstance(user, easypost.User)
    assert str.startswith(user.id, "user_")


@pytest.mark.vcr()
def test_user_update(prod_api_key):
    user = easypost.User.retrieve_me()

    test_phone = "5555555555"

    user.phone = test_phone
    user.save()

    assert isinstance(user, easypost.User)
    assert str.startswith(user.id, "user_")
    assert user.phone == test_phone


@pytest.mark.vcr()
@pytest.mark.skip(
    reason="Due to our inability to create child users securely, "
    "we must also skip deleting them as we cannot replace the deleted ones easily."
)
def test_user_delete(prod_api_key):
    user = easypost.User.create(name="Test User")

    user.delete()


@pytest.mark.vcr()
@pytest.mark.skip(reason="API keys are returned as plaintext, do not run this test.")
def test_user_all_api_keys(prod_api_key):
    user = easypost.User.retrieve_me()
    user.all_api_keys()


@pytest.mark.vcr()
@pytest.mark.skip(reason="API keys are returned as plaintext, do not run this test.")
def test_user_api_keys(prod_api_key):
    user = easypost.User.retrieve_me()
    user.api_keys()


@pytest.mark.vcr()
def test_user_update_brand(prod_api_key):
    user = easypost.User.retrieve_me()

    color = "#123456"

    brand = user.update_brand(color=color)

    assert isinstance(brand, easypost.Brand)
    assert str.startswith(brand.id, "brd_")
    assert brand.color == color
