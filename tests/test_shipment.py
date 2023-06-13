import pytest
from easypost.constant import (
    _TEST_FAILED_INTENTIONALLY_ERROR,
    NO_MORE_PAGES_ERROR,
)
from easypost.errors import (
    FilteringError,
    InvalidParameterError,
)
from easypost.models import (
    Rate,
    Shipment,
)
from easypost.util import get_lowest_smart_rate


@pytest.mark.vcr()
def test_shipment_create(full_shipment, test_client):
    shipment = test_client.shipment.create(**full_shipment)

    assert isinstance(shipment, Shipment)
    assert str.startswith(shipment.id, "shp_")
    assert shipment.rates is not None
    assert shipment.options.label_format == "PNG"
    assert shipment.options.invoice_number == "123"
    assert shipment.reference == "123"


@pytest.mark.vcr()
def test_shipment_retrieve(full_shipment, test_client):
    shipment = test_client.shipment.create(**full_shipment)

    retrieved_shipment = test_client.shipment.retrieve(shipment.id)

    assert isinstance(retrieved_shipment, Shipment)
    assert retrieved_shipment == shipment


@pytest.mark.vcr()
def test_shipment_all(page_size, test_client):
    shipments = test_client.shipment.all(page_size=page_size)

    shipment_array = shipments["shipments"]

    assert len(shipment_array) <= page_size
    assert shipments["has_more"] is not None
    assert all(isinstance(shipment, Shipment) for shipment in shipment_array)


@pytest.mark.vcr()
def test_shipment_get_next_page(page_size, test_client):
    try:
        shipments = test_client.shipment.all(page_size=page_size)
        next_page = test_client.shipment.get_next_page(shipments=shipments, page_size=page_size)

        first_id_of_first_page = shipments["shipments"][0].id
        first_id_of_second_page = next_page["shipments"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Exception as e:
        if e.message != NO_MORE_PAGES_ERROR:
            raise Exception(message=_TEST_FAILED_INTENTIONALLY_ERROR)


@pytest.mark.vcr()
def test_shipment_buy(full_shipment, test_client):
    shipment = test_client.shipment.create(**full_shipment)
    bought_shipment = test_client.shipment.buy(shipment.id, rate=shipment.lowest_rate())

    assert bought_shipment.postage_label is not None


@pytest.mark.vcr()
def test_shipment_regenerate_rates(full_shipment, test_client):
    shipment = test_client.shipment.create(**full_shipment)

    rates = test_client.shipment.regenerate_rates(shipment.id)

    rates_array = rates["rates"]

    assert isinstance(rates_array, list)
    assert all(isinstance(rate, Rate) for rate in rates_array)


@pytest.mark.vcr()
def test_shipment_convert_label(full_shipment, test_client):
    shipment = test_client.shipment.create(**full_shipment)
    bought_shipment = test_client.shipment.buy(shipment.id, rate=shipment.lowest_rate())
    shipment_with_label = test_client.shipment.label(bought_shipment.id, file_format="ZPL")

    assert shipment_with_label.postage_label.label_zpl_url is not None


@pytest.mark.vcr()
def test_shipment_insure(one_call_buy_shipment, test_client):
    """Set insurnace to `0` when buying a shipment.

    If the shipment was purchased with a USPS rate, it must have had its insurance set to `0` when bought
    so that USPS doesn't automatically insure it so we could manually insure it here.
    """
    # Set to 0 so USPS doesn't insure this automatically and we can insure the shipment manually
    one_call_buy_shipment["insurance"] = 0

    shipment = test_client.shipment.create(**one_call_buy_shipment)
    insured_shipment = test_client.shipment.insure(shipment.id, amount="100")

    assert insured_shipment.insurance == "100.00"


@pytest.mark.vcr()
def test_shipment_refund(one_call_buy_shipment, test_client):
    """Refunding a test shipment must happen within seconds of the shipment being created as test shipments naturally.

    Follow a flow of created -> delivered to cycle through tracking events in test mode - as such anything older
    than a few seconds in test mode may not be refundable.
    """
    shipment = test_client.shipment.create(**one_call_buy_shipment)
    refunded_shipment = test_client.shipment.refund(shipment.id)

    assert refunded_shipment.refund_status == "submitted"


@pytest.mark.vcr()
def test_shipment_smart_rate(basic_shipment, test_client):
    shipment = test_client.shipment.create(**basic_shipment)

    assert shipment.rates is not None

    smart_rates = test_client.shipment.get_smart_rates(shipment.id)

    assert smart_rates[0]["time_in_transit"]["percentile_50"] is not None
    assert smart_rates[0]["time_in_transit"]["percentile_75"] is not None
    assert smart_rates[0]["time_in_transit"]["percentile_85"] is not None
    assert smart_rates[0]["time_in_transit"]["percentile_90"] is not None
    assert smart_rates[0]["time_in_transit"]["percentile_95"] is not None
    assert smart_rates[0]["time_in_transit"]["percentile_97"] is not None
    assert smart_rates[0]["time_in_transit"]["percentile_99"] is not None


@pytest.mark.vcr()
def test_shipment_create_empty_objects(basic_shipment, test_client):
    shipment_data = basic_shipment
    shipment_data["customs_info"] = {}
    shipment_data["options"] = None
    shipment_data["tax_identifiers"] = None
    shipment_data["reference"] = ""

    shipment = test_client.shipment.create(**shipment_data)

    assert isinstance(shipment, Shipment)
    assert str.startswith(shipment.id, "shp_")
    assert shipment.options is not None
    assert shipment.customs_info is None
    assert shipment.reference is None


@pytest.mark.vcr()
def test_shipment_create_tax_identifier(basic_shipment, tax_identifier, test_client):
    shipment_data = basic_shipment
    shipment_data["tax_identifiers"] = [tax_identifier]

    shipment = test_client.shipment.create(**shipment_data)

    assert isinstance(shipment, Shipment)
    assert str.startswith(shipment.id, "shp_")
    assert shipment.tax_identifiers[0]["tax_id_type"] == "IOSS"


@pytest.mark.vcr()
def test_shipment_create_with_ids(ca_address_1, basic_parcel, test_client):
    from_address = test_client.address.create(**ca_address_1)
    to_address = test_client.address.create(**ca_address_1)
    parcel = test_client.parcel.create(**basic_parcel)

    shipment = test_client.shipment.create(
        from_address={"id": from_address.id},
        to_address={"id": to_address.id},
        parcel={"id": parcel.id},
    )

    assert isinstance(shipment, Shipment)
    assert str.startswith(shipment.id, "shp_")
    assert str.startswith(shipment.from_address.id, "adr_")
    assert str.startswith(shipment.to_address.id, "adr_")
    assert str.startswith(shipment.parcel.id, "prcl_")
    assert shipment.from_address.street1 == "388 Townsend St"


@pytest.mark.vcr()
def test_shipment_lowest_rate(full_shipment, test_client):
    """Test various usage alterations of the lowest_rate method."""
    shipment = test_client.shipment.create(**full_shipment)

    # Test lowest rate with no filters
    lowest_rate = shipment.lowest_rate()
    assert lowest_rate.service == "First"
    assert lowest_rate.rate == "6.07"
    assert lowest_rate.carrier == "USPS"

    # Test lowest rate with service filter (this rate is higher than the lowest but should filter)
    lowest_rate_service = shipment.lowest_rate(services=["Priority"])
    assert lowest_rate_service.service == "Priority"
    assert lowest_rate_service.rate == "7.15"
    assert lowest_rate_service.carrier == "USPS"

    # Test lowest rate with carrier filter (should error due to bad carrier)
    with pytest.raises(FilteringError) as error:
        shipment.lowest_rate(carriers=["BAD CARRIER"])
    assert str(error.value) == "No rates found."


@pytest.mark.vcr()
def test_shipment_lowest_smart_rate(basic_shipment, test_client):
    shipment = test_client.shipment.create(**basic_shipment)

    # Test lowest smart_rate with valid filters
    lowest_smart_rate_filters = test_client.shipment.lowest_smart_rate(
        shipment.id,
        delivery_days=2,
        delivery_accuracy="percentile_90",
    )
    assert lowest_smart_rate_filters["service"] == "First"
    assert lowest_smart_rate_filters["rate"] == 6.07
    assert lowest_smart_rate_filters["carrier"] == "USPS"

    # Test lowest smart_rate with invalid filters (should error due to strict delivery_days)
    with pytest.raises(FilteringError) as error:
        _ = test_client.shipment.lowest_smart_rate(
            shipment.id,
            delivery_days=0,
            delivery_accuracy="percentile_90",
        )
    assert str(error.value) == "No rates found."

    # Test lowest smart_rate with invalid filters (should error due to invalid delivery_accuracy)
    with pytest.raises(InvalidParameterError) as error:
        _ = test_client.shipment.lowest_smart_rate(
            shipment.id,
            delivery_days=3,
            delivery_accuracy="BAD_ACCURACY",
        )
    assert "Invalid delivery_accuracy value" in str(error.value)


@pytest.mark.vcr()
def test_shipment_get_lowest_smart_rate(basic_shipment, test_client):
    shipment = test_client.shipment.create(**basic_shipment)
    smart_rates = test_client.shipment.get_smart_rates(shipment.id)

    # Test lowest smart_rate with valid filters
    lowest_smart_rate_filters = get_lowest_smart_rate(
        smart_rates,
        delivery_days=2,
        delivery_accuracy="percentile_90",
    )
    assert lowest_smart_rate_filters["service"] == "First"
    assert lowest_smart_rate_filters["rate"] == 6.07
    assert lowest_smart_rate_filters["carrier"] == "USPS"

    # Test lowest smart_rate with invalid filters (should error due to strict delivery_days)
    with pytest.raises(FilteringError) as error:
        _ = get_lowest_smart_rate(
            smart_rates,
            delivery_days=0,
            delivery_accuracy="percentile_90",
        )
    assert str(error.value) == "No rates found."

    # Test lowest smart_rate with invalid filters (should error due to bad delivery_accuracy)
    with pytest.raises(InvalidParameterError) as error:
        _ = get_lowest_smart_rate(
            smart_rates,
            delivery_days=3,
            delivery_accuracy="BAD_ACCURACY",
        )
    assert "Invalid delivery_accuracy value" in str(error.value)


@pytest.mark.vcr()
def test_shipment_generate_form(one_call_buy_shipment, rma_form_options, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)
    form_type = "return_packing_slip"

    shipment_with_form = test_client.shipment.generate_form(
        shipment.id,
        form_type,
        rma_form_options,
    )

    assert len(shipment_with_form.forms) > 0

    form = shipment_with_form.forms[0]

    assert form.form_type == form_type
    assert form.form_url is not None


@pytest.mark.vcr()
def test_shipment_create_with_carbon_offset(basic_shipment, test_client):
    shipment = test_client.shipment.create(with_carbon_offset=True, **basic_shipment)

    assert isinstance(shipment, Shipment)
    assert shipment.rates is not None
    assert all(rate.carbon_offset is not None for rate in shipment.rates)


@pytest.mark.vcr()
def test_shipment_buy_with_carbon_offset(basic_shipment, test_client):
    shipment = test_client.shipment.create(**basic_shipment)
    bought_shipment = test_client.shipment.buy(shipment.id, rate=shipment.lowest_rate(), with_carbon_offset=True)

    assert isinstance(bought_shipment, Shipment)
    assert any(fee.type == "CarbonOffsetFee" for fee in bought_shipment.fees)


@pytest.mark.vcr()
def test_shipment_one_call_buy_with_carbon_offset(one_call_buy_shipment, test_client):
    shipment = test_client.shipment.create(with_carbon_offset=True, **one_call_buy_shipment)

    assert isinstance(shipment, Shipment)
    assert all(rate.carbon_offset is not None for rate in shipment.rates)


@pytest.mark.vcr()
def test_shipment_rerate_with_carbon_offset(one_call_buy_shipment, test_client):
    shipment = test_client.shipment.create(**one_call_buy_shipment)

    new_carbon_rates = test_client.shipment.regenerate_rates(shipment.id, with_carbon_offset=True)

    assert all(rate.carbon_offset is not None for rate in new_carbon_rates.rates)


@pytest.mark.vcr()
def test_shipment_buy_with_end_shipper_id(ca_address_1, basic_shipment, test_client):
    end_shipper = test_client.end_shipper.create(**ca_address_1)

    shipment = test_client.shipment.create(**basic_shipment)
    bought_shipment = test_client.shipment.buy(
        shipment.id, rate=shipment.lowest_rate(), end_shipper_id=end_shipper["id"]
    )

    assert bought_shipment.postage_label is not None


@pytest.mark.vcr()
def test_retrieve_estimated_delivery_date(basic_shipment, planned_ship_date, test_client):
    """Tests that we retrieve time-in-transit data for each of the Rates of a Shipment."""
    shipment = test_client.shipment.create(**basic_shipment)

    rates = test_client.shipment.retrieve_estimated_delivery_date(shipment.id, planned_ship_date=planned_ship_date)

    assert all(entry.get("easypost_time_in_transit_data") for entry in rates)
