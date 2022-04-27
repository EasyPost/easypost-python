import pytest

import easypost


@pytest.mark.vcr()
def test_shipment_create(full_shipment):
    shipment = easypost.Shipment.create(**full_shipment)

    assert isinstance(shipment, easypost.Shipment)
    assert str.startswith(shipment.id, "shp_")
    assert shipment.rates is not None
    assert shipment.options.label_format == "PNG"
    assert shipment.options.invoice_number == "123"
    assert shipment.reference == "123"


@pytest.mark.vcr()
def test_shipment_retrieve(full_shipment):
    shipment = easypost.Shipment.create(**full_shipment)

    retrieved_shipment = easypost.Shipment.retrieve(shipment.id)

    assert isinstance(retrieved_shipment, easypost.Shipment)
    assert retrieved_shipment == shipment


@pytest.mark.vcr()
def test_shipment_all(page_size):
    shipments = easypost.Shipment.all(page_size=page_size)

    shipment_array = shipments["shipments"]

    assert len(shipment_array) <= page_size
    assert shipments["has_more"] is not None
    assert all(isinstance(shipment, easypost.Shipment) for shipment in shipment_array)


@pytest.mark.vcr()
def test_shipment_buy(full_shipment):
    shipment = easypost.Shipment.create(**full_shipment)
    shipment.buy(rate=shipment.lowest_rate())

    assert shipment.postage_label is not None


@pytest.mark.vcr()
def test_shipment_regenerate_rates(full_shipment):
    shipment = easypost.Shipment.create(**full_shipment)

    rates = shipment.regenerate_rates()

    rates_array = rates["rates"]

    assert isinstance(rates_array, list)
    assert all(isinstance(rate, easypost.Rate) for rate in rates_array)


@pytest.mark.vcr()
def test_shipment_convert_label(full_shipment):
    shipment = easypost.Shipment.create(**full_shipment)
    shipment.buy(rate=shipment.lowest_rate())
    shipment.label(file_format="ZPL")

    assert shipment.postage_label.label_zpl_url is not None


@pytest.mark.vcr()
def test_shipment_insure(one_call_buy_shipment):
    """Set insurnace to `0` when buying a shipment.

    If the shipment was purchased with a USPS rate, it must have had its insurance set to `0` when bought
    so that USPS doesn't automatically insure it so we could manually insure it here.
    """
    # Set to 0 so USPS doesn't insure this automatically and we can insure the shipment manually
    one_call_buy_shipment["insurance"] = 0

    shipment = easypost.Shipment.create(**one_call_buy_shipment)
    shipment.insure(amount="100")

    assert shipment.insurance == "100.00"


@pytest.mark.vcr()
def test_shipment_refund(one_call_buy_shipment):
    """Refunding a test shipment must happen within seconds of the shipment being created as test shipments naturally.

    Follow a flow of created -> delivered to cycle through tracking events in test mode - as such anything older
    than a few seconds in test mode may not be refundable.
    """
    shipment = easypost.Shipment.create(**one_call_buy_shipment)
    shipment.refund()

    assert shipment.refund_status == "submitted"


@pytest.mark.vcr()
def test_shipment_smartrate(basic_shipment):
    shipment = easypost.Shipment.create(**basic_shipment)

    assert shipment.rates is not None

    smartrates = shipment.get_smartrates()

    assert smartrates[0]["time_in_transit"]["percentile_50"] is not None
    assert smartrates[0]["time_in_transit"]["percentile_75"] is not None
    assert smartrates[0]["time_in_transit"]["percentile_85"] is not None
    assert smartrates[0]["time_in_transit"]["percentile_90"] is not None
    assert smartrates[0]["time_in_transit"]["percentile_95"] is not None
    assert smartrates[0]["time_in_transit"]["percentile_97"] is not None
    assert smartrates[0]["time_in_transit"]["percentile_99"] is not None


@pytest.mark.vcr()
def test_shipment_create_empty_objects(basic_shipment):
    shipment_data = basic_shipment
    shipment_data["customs_info"] = {}
    shipment_data["customs_info"]["customs_item"] = {}
    shipment_data["options"] = None
    shipment_data["tax_identifiers"] = None
    shipment_data["reference"] = ""

    shipment = easypost.Shipment.create(**shipment_data)

    assert isinstance(shipment, easypost.Shipment)
    assert str.startswith(shipment.id, "shp_")
    assert shipment.options is not None
    assert shipment.customs_info is None
    assert shipment.reference is None


@pytest.mark.vcr()
def test_shipment_create_tax_identifier(basic_shipment, tax_identifier):
    shipment_data = basic_shipment
    shipment_data["tax_identifiers"] = [tax_identifier]

    shipment = easypost.Shipment.create(**shipment_data)

    assert isinstance(shipment, easypost.Shipment)
    assert str.startswith(shipment.id, "shp_")
    assert shipment.tax_identifiers[0]["tax_id_type"] == "IOSS"


@pytest.mark.vcr()
def test_shipment_create_with_ids(basic_address, basic_parcel):
    from_address = easypost.Address.create(**basic_address)
    to_address = easypost.Address.create(**basic_address)
    parcel = easypost.Parcel.create(**basic_parcel)

    shipment = easypost.Shipment.create(
        from_address={"id": from_address.id},
        to_address={"id": to_address.id},
        parcel={"id": parcel.id},
    )

    assert isinstance(shipment, easypost.Shipment)
    assert str.startswith(shipment.id, "shp_")
    assert str.startswith(shipment.from_address.id, "adr_")
    assert str.startswith(shipment.to_address.id, "adr_")
    assert str.startswith(shipment.parcel.id, "prcl_")
    assert shipment.from_address.street1 == "388 Townsend St"


@pytest.mark.vcr()
def test_shipment_lowest_rate(full_shipment):
    """Test various usage alterations of the lowest_rate method."""
    shipment = easypost.Shipment.create(**full_shipment)

    # Test lowest rate with no filters
    lowest_rate = shipment.lowest_rate()
    assert lowest_rate.service == "First"
    assert lowest_rate.rate == "5.49"
    assert lowest_rate.carrier == "USPS"

    # Test lowest rate with service filter (this rate is higher than the lowest but should filter)
    lowest_rate_service = shipment.lowest_rate(services=["Priority"])
    assert lowest_rate_service.service == "Priority"
    assert lowest_rate_service.rate == "7.37"
    assert lowest_rate_service.carrier == "USPS"

    # Test lowest rate with carrier filter (should error due to bad carrier)
    with pytest.raises(easypost.Error) as error:
        shipment.lowest_rate(carriers=["BAD CARRIER"])
        assert error.message == "No rates found."


@pytest.mark.vcr()
def test_shipment_lowest_smartrate(basic_shipment):
    shipment = easypost.Shipment.create(**basic_shipment)
    lowest_smartrate = shipment.lowest_smartrate()

    assert lowest_smartrate["service"] == "First"
    assert lowest_smartrate["rate"] == 5.49
    assert lowest_smartrate["carrier"] == "USPS"

    # Test lowest rate with filters
    lowest_smartrate_filters = shipment.lowest_smartrate(delivery_days=1, delivery_accuracy="percentile_90")
    assert lowest_smartrate_filters["service"] == "Priority"
    assert lowest_smartrate_filters["rate"] == 7.37
    assert lowest_smartrate_filters["carrier"] == "USPS"

    # Test lowest rate with filters (should error due to bad delivery_accuracy)
    with pytest.raises(easypost.Error) as error:
        lowest_smartrate_filters = shipment.lowest_smartrate(delivery_days=1, delivery_accuracy="BAD_PERCENTILE")
        assert error.message == "No rates found."


@pytest.mark.vcr()
def test_shipment_get_lowest_smartrate(basic_shipment):
    shipment = easypost.Shipment.create(**basic_shipment)
    smartrates = shipment.get_smartrates()

    lowest_smartrate = easypost.Shipment.get_lowest_smartrate(smartrates)
    assert lowest_smartrate["service"] == "First"
    assert lowest_smartrate["rate"] == 5.49
    assert lowest_smartrate["carrier"] == "USPS"

    # Test lowest rate with filters
    lowest_smartrate_filters = easypost.Shipment.get_lowest_smartrate(
        smartrates, delivery_days=1, delivery_accuracy="percentile_90"
    )
    assert lowest_smartrate_filters["service"] == "Priority"
    assert lowest_smartrate_filters["rate"] == 7.37
    assert lowest_smartrate_filters["carrier"] == "USPS"

    # Test lowest rate with filters (should error due to bad delivery_accuracy)
    with pytest.raises(easypost.Error) as error:
        lowest_smartrate_filters = easypost.Shipment.get_lowest_smartrate(
            smartrates, delivery_days=1, delivery_accuracy="BAD_PERCENTILE"
        )
        assert error.message == "No rates found."
