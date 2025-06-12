import pytest


@pytest.mark.vcr()
def test_luma_recommend_service(
    basic_shipment,
    luma_ruleset_name,
    luma_planned_ship_date,
    luma_deliver_by_date,
    test_client,
):
    """Test that we get service recommendations from Luma."""
    basic_shipment["ruleset_name"] = luma_ruleset_name
    basic_shipment["planned_ship_date"] = luma_planned_ship_date
    basic_shipment["deliver_by_date"] = luma_deliver_by_date

    recommendations = test_client.luma.recommend_service(**basic_shipment)

    assert recommendations.luma_info.luma_selected_rate is not None
