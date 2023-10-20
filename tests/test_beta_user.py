import pytest

import easypost

@pytest.mark.vcr()
def test_beta_user_retrieve_all_children(prod_api_key, page_size):
    children_data = easypost.beta.User.retrieve_all_children(page_size=page_size)

    children_array = children_data["children"]
    assert len(children_array) <= page_size
    assert all(isinstance(child, easypost.User) for child in children_array)

    has_more = children_data["has_more"]
    assert isinstance(has_more, bool)

@pytest.mark.vcr()
def test_beta_user_get_next_page(prod_api_key, page_size):
    try:
        children = easypost.beta.User.retrieve_all_children(page_size=page_size)
        next_page = easypost.beta.User.get_next_page_of_children(children=children, page_size=page_size)

        first_id_of_first_page = children["children"][0].id
        first_id_of_second_page = next_page["children"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except easypost.Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise easypost.Error(message="Test failed intentionally.")
