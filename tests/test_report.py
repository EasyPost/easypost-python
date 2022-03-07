import pytest

import easypost


def create_report(report_type, report_start_date, report_end_date):
    return easypost.Report.create(
        type=report_type,
        start_date=report_start_date,
        end_date=report_end_date,
    )


@pytest.mark.vcr()
def test_report_create_payment_log_report(report_start_date, report_end_date):
    report = create_report("payment_log", report_start_date, report_end_date)

    assert isinstance(report, easypost.Report)
    assert str.startswith(report.id, "plrep_")


@pytest.mark.vcr()
def test_report_create_refund_report(report_start_date, report_end_date):
    report = create_report("refund", report_start_date, report_end_date)

    assert isinstance(report, easypost.Report)
    assert str.startswith(report.id, "refrep_")


@pytest.mark.vcr()
def test_report_create_shipment_report(report_start_date, report_end_date):
    report = create_report("shipment", report_start_date, report_end_date)

    assert isinstance(report, easypost.Report)
    assert str.startswith(report.id, "shprep_")


@pytest.mark.vcr()
def test_report_create_shipment_invoice_report(report_start_date, report_end_date):
    report = create_report("shipment_invoice", report_start_date, report_end_date)

    assert isinstance(report, easypost.Report)
    assert str.startswith(report.id, "shpinvrep_")


@pytest.mark.vcr()
def test_report_create_tracker_report(report_start_date, report_end_date):
    report = create_report("tracker", report_start_date, report_end_date)

    assert isinstance(report, easypost.Report)
    assert str.startswith(report.id, "trkrep_")


@pytest.mark.vcr()
def test_report_retrieve_payment_log_report(report_start_date, report_end_date):
    report = create_report("payment_log", report_start_date, report_end_date)

    retrieved_report = easypost.Report.retrieve(report.id)

    assert isinstance(retrieved_report, easypost.Report)
    assert report.start_date == retrieved_report.start_date
    assert report.end_date == retrieved_report.end_date


@pytest.mark.vcr()
def test_report_retrieve_refund_report(report_start_date, report_end_date):
    report = create_report("refund", report_start_date, report_end_date)

    retrieved_report = easypost.Report.retrieve(report.id)

    assert isinstance(retrieved_report, easypost.Report)
    assert report.start_date == retrieved_report.start_date
    assert report.end_date == retrieved_report.end_date


@pytest.mark.vcr()
def test_report_retrieve_shipment_report(report_start_date, report_end_date):
    report = create_report("shipment", report_start_date, report_end_date)

    retrieved_report = easypost.Report.retrieve(report.id)

    assert isinstance(retrieved_report, easypost.Report)
    assert report.start_date == retrieved_report.start_date
    assert report.end_date == retrieved_report.end_date


@pytest.mark.vcr()
def test_report_retrieve_shipment_invoice_report(report_start_date, report_end_date):
    report = create_report("shipment_invoice", report_start_date, report_end_date)

    retrieved_report = easypost.Report.retrieve(report.id)

    assert isinstance(retrieved_report, easypost.Report)
    assert report.start_date == retrieved_report.start_date
    assert report.end_date == retrieved_report.end_date


@pytest.mark.vcr()
def test_report_retrieve_tracker_report(report_start_date, report_end_date):
    report = create_report("tracker", report_start_date, report_end_date)

    retrieved_report = easypost.Report.retrieve(report.id)

    assert isinstance(retrieved_report, easypost.Report)
    assert report.start_date == retrieved_report.start_date
    assert report.end_date == retrieved_report.end_date


@pytest.mark.vcr()
def test_report_all(page_size):
    reports = easypost.Report.all(type="shipment", page_size=page_size)

    reports_array = reports["reports"]

    assert len(reports_array) <= page_size
    assert reports["has_more"] is not None
    assert all(isinstance(report, easypost.Report) for report in reports_array)
