from unittest.mock import patch

import pytest
from easypost.constant import NO_MORE_PAGES_ERROR
from easypost.errors import EndOfPaginationError


@pytest.mark.vcr()  # Cassette not needed due to mocking, but used to avoid making real bogus API calls
def test_get_next_page_collects_all_pages(test_client):
    page_size = 1  # Doesn't matter what this is, we're mocking the response
    all_results = []

    # Using scanforms as an example, but this should work for any service since it's a base class method
    first_page_response = {
        "scan_forms": [
            {
                "id": "sf_123",
            }
        ],
        "has_more": True,
    }

    # Mock the initial "get all scanforms" call
    with patch("easypost.requestor.Requestor.request", return_value=first_page_response):
        first_page = test_client.scan_form.all(page_size=page_size)
        all_results += first_page["scan_forms"]
        previous_page = first_page

    second_page_response = {
        "scan_forms": [
            {
                "id": "sf_456",
            }
        ],
        "has_more": True,
    }

    # Mock the first "get next page" call with more to collect after
    # (current page "has_more" = True, next page "has_more" = True)
    with patch("easypost.requestor.Requestor.request", return_value=second_page_response):
        next_page = test_client.scan_form.get_next_page(scan_forms=previous_page, page_size=page_size)  # type: ignore
        all_results += next_page["scan_forms"]
        previous_page = next_page

    third_page_response = {
        "scan_forms": [
            {
                "id": "sf_789",
            }
        ],
        "has_more": False,
    }

    # Mock the second "get next page" call with no more to collect
    # (current page "has_more" = True, next page "has_more" = False)
    with patch("easypost.requestor.Requestor.request", return_value=third_page_response):
        next_page = test_client.scan_form.get_next_page(scan_forms=previous_page, page_size=page_size)  # type: ignore
        all_results += next_page["scan_forms"]
        previous_page = next_page

    # Verify we have all scan_forms (from the initial "get all scanforms" and two subsequent "get next page" calls)
    # Ensures that no guard clauses inside the "get next page" method are preventing us from collecting all scanforms
    assert len(all_results) == 3

    # Now that the previous page has "has_more" = False, it should throw an error before even making the API call
    with pytest.raises(EndOfPaginationError) as error:
        _ = test_client.scan_form.get_next_page(scan_forms=previous_page, page_size=page_size)  # type: ignore

    assert error.value.message == NO_MORE_PAGES_ERROR
