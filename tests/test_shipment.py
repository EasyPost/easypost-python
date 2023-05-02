import pytest

import easypost
from easypost.error import Error


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
def test_shipment_get_next_page(page_size):
    try:
        shipments = easypost.Shipment.all(page_size=page_size)
        next_page = easypost.Shipment.get_next_page(shipments=shipments, page_size=page_size)

        first_id_of_first_page = shipments["shipments"][0].id
        first_id_of_second_page = next_page["shipments"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise Error(message="Test failed intentionally.")


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
def test_shipment_create_with_ids(ca_address_1, basic_parcel):
    from_address = easypost.Address.create(**ca_address_1)
    to_address = easypost.Address.create(**ca_address_1)
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
    assert lowest_rate.rate == "5.57"
    assert lowest_rate.carrier == "USPS"

    # Test lowest rate with service filter (this rate is higher than the lowest but should filter)
    lowest_rate_service = shipment.lowest_rate(services=["Priority"])
    assert lowest_rate_service.service == "Priority"
    assert lowest_rate_service.rate == "7.90"
    assert lowest_rate_service.carrier == "USPS"

    # Test lowest rate with carrier filter (should error due to bad carrier)
    with pytest.raises(easypost.Error) as error:
        shipment.lowest_rate(carriers=["BAD CARRIER"])
    assert str(error.value) == "No rates found."


@pytest.mark.vcr()
def test_shipment_lowest_smartrate(basic_shipment):
    shipment = easypost.Shipment.create(**basic_shipment)

    # Test lowest smartrate with valid filters
    lowest_smartrate_filters = shipment.lowest_smartrate(delivery_days=2, delivery_accuracy="percentile_90")
    assert lowest_smartrate_filters["service"] == "First"
    assert lowest_smartrate_filters["rate"] == 5.57
    assert lowest_smartrate_filters["carrier"] == "USPS"

    # Test lowest smartrate with invalid filters (should error due to strict delivery_days)
    with pytest.raises(easypost.Error) as error:
        _ = shipment.lowest_smartrate(delivery_days=0, delivery_accuracy="percentile_90")
    assert str(error.value) == "No rates found."

    # Test lowest smartrate with invalid filters (should error due to invalid delivery_accuracy)
    with pytest.raises(easypost.Error) as error:
        _ = shipment.lowest_smartrate(delivery_days=3, delivery_accuracy="BAD_ACCURACY")
    assert "Invalid delivery_accuracy value" in str(error.value)


@pytest.mark.vcr()
def test_shipment_get_lowest_smartrate(basic_shipment):
    shipment = easypost.Shipment.create(**basic_shipment)
    smartrates = shipment.get_smartrates()

    # Test lowest smartrate with valid filters
    lowest_smartrate_filters = easypost.Shipment.get_lowest_smartrate(
        smartrates, delivery_days=2, delivery_accuracy="percentile_90"
    )
    assert lowest_smartrate_filters["service"] == "First"
    assert lowest_smartrate_filters["rate"] == 5.57
    assert lowest_smartrate_filters["carrier"] == "USPS"

    # Test lowest smartrate with invalid filters (should error due to strict delivery_days)
    with pytest.raises(easypost.Error) as error:
        _ = easypost.Shipment.get_lowest_smartrate(smartrates, delivery_days=0, delivery_accuracy="percentile_90")
    assert str(error.value) == "No rates found."

    # Test lowest smartrate with invalid filters (should error due to bad delivery_accuracy)
    with pytest.raises(easypost.Error) as error:
        _ = easypost.Shipment.get_lowest_smartrate(smartrates, delivery_days=3, delivery_accuracy="BAD_ACCURACY")
    assert "Invalid delivery_accuracy value" in str(error.value)


@pytest.mark.vcr()
def test_generate_form(one_call_buy_shipment, rma_form_options):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)
    form_type = "return_packing_slip"

    shipment.generate_form(
        form_type,
        rma_form_options,
    )

    assert len(shipment.forms) > 0

    form = shipment.forms[0]

    assert form.form_type == form_type
    assert form.form_url is not None


@pytest.mark.vcr()
def test_shipment_create_with_carbon_offset(basic_shipment):
    shipment = easypost.Shipment.create(with_carbon_offset=True, **basic_shipment)

    assert isinstance(shipment, easypost.Shipment)
    assert shipment.rates is not None
    assert all(rate.carbon_offset is not None for rate in shipment.rates)


@pytest.mark.vcr()
def test_shipment_buy_with_carbon_offset(basic_shipment):
    shipment = easypost.Shipment.create(**basic_shipment)
    shipment.buy(rate=shipment.lowest_rate(), with_carbon_offset=True)

    assert isinstance(shipment, easypost.Shipment)
    assert any(fee.type == "CarbonOffsetFee" for fee in shipment.fees)


@pytest.mark.vcr()
def test_shipment_one_call_buy_with_carbon_offset(one_call_buy_shipment):
    shipment = easypost.Shipment.create(with_carbon_offset=True, **one_call_buy_shipment)

    assert isinstance(shipment, easypost.Shipment)
    assert all(rate.carbon_offset is not None for rate in shipment.rates)


@pytest.mark.vcr()
def test_shipment_rerate_with_carbon_offset(one_call_buy_shipment):
    shipment = easypost.Shipment.create(**one_call_buy_shipment)

    new_carbon_rates = shipment.regenerate_rates(with_carbon_offset=True)

    assert all(rate.carbon_offset is not None for rate in new_carbon_rates.rates)


@pytest.mark.vcr()
def test_shipment_buy_with_end_shipper_id(ca_address_1, basic_shipment):
    end_shipper = easypost.EndShipper.create(**ca_address_1)

    shipment = easypost.Shipment.create(**basic_shipment)
    shipment.buy(rate=shipment.lowest_rate(), end_shipper_id=end_shipper["id"])

    assert shipment.postage_label is not None


@pytest.mark.vcr()
def test_retrieve_estimated_delivery_date(basic_shipment, planned_ship_date):
    """Tests that we retrieve time-in-transit data for each of the Rates of a Shipment."""
    shipment = easypost.Shipment.create(**basic_shipment)

    rates = shipment.retrieve_estimated_delivery_date(planned_ship_date=planned_ship_date)

    assert all(entry.get("easypost_time_in_transit_data") for entry in rates)
