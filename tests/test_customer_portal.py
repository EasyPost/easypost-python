import pytest


@pytest.mark.vcr()
def test_customer_portal_account_link_create(full_shipment, basic_claim, prod_client):
    user = prod_client.user.all_children()["children"][0]

    account_link = prod_client.customer_portal.create_account_link(
        session_type="account_onboarding",
        user_id=user.id,
        refresh_url="https://example.com/refresh",
        return_url="https://example.com/return",
    )

    assert account_link.object == "CustomerPortalAccountLink"
