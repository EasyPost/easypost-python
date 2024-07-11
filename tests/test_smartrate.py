import pytest


@pytest.mark.vcr()
def test_smartrate_estimate_delivery_date(
    basic_shipment,
    ca_address_1,
    ca_address_2,
    planned_ship_date,
    usps,
    test_client,
):
    """Test that we retrieve SmartRates when provided a from/to zip and planned ship date."""
    params = {
        "from_zip": ca_address_1["zip"],
        "to_zip": ca_address_2["zip"],
        "planned_ship_date": planned_ship_date,
        "carriers": [usps],
    }

    rates = test_client.smart_rate.estimate_delivery_date(**params)

    assert all(entry.get("easypost_time_in_transit_data") for entry in rates["results"])


@pytest.mark.vcr()
def test_smartrate_recommend_ship_date(
    basic_shipment,
    ca_address_1,
    ca_address_2,
    desired_delivery_date,
    usps,
    test_client,
):
    """Test that we retrieve SmartRates when provided a from/to zip and desired delivery date."""
    params = {
        "from_zip": ca_address_1["zip"],
        "to_zip": ca_address_2["zip"],
        "desired_delivery_date": desired_delivery_date,
        "carriers": [usps],
    }

    rates = test_client.smart_rate.recommend_ship_date(**params)

    assert all(entry.get("easypost_time_in_transit_data") for entry in rates["results"])
