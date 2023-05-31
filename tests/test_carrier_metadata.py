import pytest


@pytest.mark.vcr()
def test_retrieve_carrier_metadata(test_client):
    """Tests that we can retrieve all carriers and all metadata from the API when no params are provided."""
    carrier_metadata = test_client.carrier_metadata.retrieve()

    # Assert we get multiple carriers
    assert any(carrier.name == "usps" for carrier in carrier_metadata)
    assert any(carrier.name == "fedex" for carrier in carrier_metadata)


@pytest.mark.vcr()
def test_retrieve_carrier_metadata_with_filters(test_client):
    """Tests that we can retrieve metadata based on the filters provided."""
    carrier_metadata = test_client.carrier_metadata.retrieve(
        carriers=["usps"],
        types=["service_levels", "predefined_packages"],
    )

    # Assert we get the single carrier we asked for and only the types we asked for
    assert all(carrier.name == "usps" for carrier in carrier_metadata)
    assert len(carrier_metadata) == 1
    assert carrier_metadata[0]["service_levels"]
    assert carrier_metadata[0]["predefined_packages"]
    assert not carrier_metadata[0].get("supported_features")
