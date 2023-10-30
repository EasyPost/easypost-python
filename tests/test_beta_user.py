from unittest.mock import patch

import pytest

import easypost


@pytest.mark.vcr()
def test_beta_user_all_children(prod_api_key, page_size):
    children_data = easypost.beta.User.all_children(page_size=page_size)

    children_array = children_data["children"]
    assert len(children_array) <= page_size
    assert all(isinstance(child, easypost.User) for child in children_array)

    has_more = children_data["has_more"]
    assert isinstance(has_more, bool)


@pytest.mark.vcr()
def test_beta_user_get_next_page(prod_api_key, page_size):
    try:
        children = easypost.beta.User.all_children(page_size=page_size)
        next_page = easypost.beta.User.get_next_page_of_children(children=children, page_size=page_size)

        first_id_of_first_page = children["children"][0].id
        first_id_of_second_page = next_page["children"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except easypost.Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise easypost.Error(message="Test failed intentionally.")


@pytest.mark.vcr()  # Cassette not needed due to mocking, but used to avoid making real bogus API calls
def test_beta_user_get_next_page_collect_all(prod_api_key):
    page_size = 1  # Doesn't matter what this is, we're mocking the response
    all_children = []

    first_page_response = {
        "children": [
            {
                "id": "user_123",
            }
        ],
        "has_more": True,
    }

    # Mock the initial "get all children" call
    return_value = (first_page_response, prod_api_key)
    with patch("easypost.requestor.Requestor.request", return_value=return_value):
        first_page = easypost.beta.User.all_children(page_size=page_size)
        all_children += first_page["children"]
        previous_page = first_page

    second_page_response = {
        "children": [
            {
                "id": "user_456",
            }
        ],
        "has_more": True,
    }

    # Mock the first "get next page" call with more to collect after
    # (current page "has_more" = True, next page "has_more" = True)
    return_value = (second_page_response, prod_api_key)
    with patch("easypost.requestor.Requestor.request", return_value=return_value):
        next_page = easypost.beta.User.get_next_page_of_children(
            children=previous_page, page_size=page_size  # type: ignore
        )
        all_children += next_page["children"]
        previous_page = next_page

    third_page_response = {
        "children": [
            {
                "id": "user_789",
            }
        ],
        "has_more": False,
    }

    # Mock the second "get next page" call with no more to collect
    # (current page "has_more" = True, next page "has_more" = False)
    return_value = (third_page_response, prod_api_key)
    with patch("easypost.requestor.Requestor.request", return_value=return_value):
        next_page = easypost.beta.User.get_next_page_of_children(
            children=previous_page, page_size=page_size  # type: ignore
        )
        all_children += next_page["children"]
        previous_page = next_page

    # Verify we have all children (from both the "get all children" and "get next page" calls)
    # Ensures that no guard clauses inside the "get next page" method are preventing us from collecting all children
    assert len(all_children) == 3

    # Now that the previous page has "has_more" = False, it should throw an error before even making the API call
    with pytest.raises(easypost.Error) as error:
        _ = easypost.beta.User.get_next_page_of_children(children=previous_page, page_size=page_size)  # type: ignore

    assert str(error.value) == "There are no more pages to retrieve."
