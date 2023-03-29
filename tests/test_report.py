import pytest

import easypost
from easypost.error import Error


@pytest.mark.vcr()
def test_report_create_report(report_type, report_date):
    report = easypost.Report.create(
        type=report_type,
        start_date=report_date,
        end_date=report_date,
    )

    assert isinstance(report, easypost.Report)
    assert str.startswith(report.id, "shprep_")


@pytest.mark.vcr()
def test_report_create_with_additional_columns(report_type, report_date):
    report = easypost.Report.create(
        type=report_type,
        start_date=report_date,
        end_date=report_date,
        additional_columns=["from_name", "from_company"],
    )

    # Reports are queued, so we can't wait for completion.
    # Verifying columns would require parsing CSV. Verify correct parameters via URL in cassette
    assert isinstance(report, easypost.Report)


@pytest.mark.vcr()
def test_report_create_with_columns(report_type, report_date):
    report = easypost.Report.create(
        type=report_type,
        start_date=report_date,
        end_date=report_date,
        columns=["usps_zone"],
    )

    # Reports are queued, so we can't wait for completion.
    # Verifying columns would require parsing CSV. Verify correct parameters via URL in cassette
    assert isinstance(report, easypost.Report)


@pytest.mark.vcr()
def test_report_retrieve_shipment_report(report_type, report_date):
    report = easypost.Report.create(
        type=report_type,
        start_date=report_date,
        end_date=report_date,
    )

    retrieved_report = easypost.Report.retrieve(report.id)

    assert isinstance(retrieved_report, easypost.Report)
    assert report.start_date == retrieved_report.start_date
    assert report.end_date == retrieved_report.end_date


@pytest.mark.vcr()
def test_report_all(report_type, page_size):
    reports = easypost.Report.all(type=report_type, page_size=page_size)

    reports_array = reports["reports"]

    assert len(reports_array) <= page_size
    assert reports["has_more"] is not None
    assert all(isinstance(report, easypost.Report) for report in reports_array)


@pytest.mark.vcr()
def test_report_get_next_page(report_type, page_size):
    try:
        reports = easypost.Report.all(type=report_type, page_size=page_size)
        next_page = easypost.Report.get_next_page(reports=reports, page_size=page_size)

        first_id_of_first_page = reports["reports"][0].id
        first_id_of_second_page = next_page["reports"][0].id

        assert first_id_of_first_page != first_id_of_second_page
    except Error as e:
        if e.message != "There are no more pages to retrieve.":
            raise Error(message="Test failed intentionally.")
