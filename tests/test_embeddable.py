import pytest


@pytest.mark.vcr()
def test_embeddable_session_create(full_shipment, basic_claim, prod_client):
    user = prod_client.user.all_children()["children"][0]

    session = prod_client.embeddable.create_session(
        origin_host="https://example.com",
        user_id=user.id,
    )

    assert session.object == "EmbeddablesSession"
