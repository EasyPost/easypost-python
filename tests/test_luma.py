import pytest


@pytest.mark.vcr()
def test_luma_get_promise(
    basic_shipment,
    luma_ruleset_name,
    luma_planned_ship_date,
    test_client,
):
    """Test that we get service recommendations from Luma based on your ruleset."""
    basic_shipment["ruleset_name"] = luma_ruleset_name
    basic_shipment["planned_ship_date"] = luma_planned_ship_date

    recommendations = test_client.luma.get_promise(**basic_shipment)

    assert recommendations.luma_info.luma_selected_rate is not None
