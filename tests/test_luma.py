import pytest


@pytest.mark.vcr()
def test_luma_get_promises(
    basic_shipment,
    luma_ruleset_name,
    luma_planned_ship_date,
    luma_deliver_by_date,
    test_client,
):
    """Test that we get promises from Luma."""
    basic_shipment["ruleset_name"] = luma_ruleset_name
    basic_shipment["planned_ship_date"] = luma_planned_ship_date
    basic_shipment["deliver_by_date"] = luma_deliver_by_date

    promises = test_client.luma.get_promises(**basic_shipment)

    assert promises.luma_info.luma_selected_rate is not None
