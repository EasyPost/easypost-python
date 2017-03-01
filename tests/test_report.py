# Unit tests related to 'Report's (https://www.easypost.com/docs/api.html#reports).

import easypost


def test_shipment_report():
    report = easypost.Report.create(
        start_date="2012-12-01",
        end_date="2013-01-01",
        type="shipment"
    )

    assert report.object == "ShipmentReport"
    assert report.status == "available"
    assert report.__class__ == easypost.Report

    report2 = easypost.Report.retrieve(report.id)

    assert report2.__class__ == easypost.Report
    assert report2.id == report.id

    reports = easypost.Report.all(type="shipment")
    assert len(reports["reports"])
    assert reports["reports"][0].id == report.id == report2.id


def test_payment_log_report():
    report = easypost.Report.create(
        start_date="2012-12-01",
        end_date="2013-01-01",
        type="payment_log"
    )

    assert report.object == "PaymentLogReport"
    assert report.status == "available"
    assert report.__class__ == easypost.Report

    report2 = easypost.Report.retrieve(report.id)

    assert report2.__class__ == easypost.Report
    assert report2.id == report.id

    reports = easypost.Report.all(type="payment_log")
    assert len(reports["reports"])
    assert reports["reports"][0].id == report.id == report2.id


def test_tracker_report():
    report = easypost.Report.create(
        start_date="2012-12-01",
        end_date="2013-01-01",
        type="tracker"
    )

    assert report.object == "TrackerReport"
    # assert report.status == "available" # Not yet implemented for tracker reports
    assert report.__class__ == easypost.Report

    report2 = easypost.Report.retrieve(report.id)

    assert report2.__class__ == easypost.Report
    assert report2.id == report.id

    reports = easypost.Report.all(type="tracker")
    assert len(reports["reports"])
    assert reports["reports"][0].id == report.id == report2.id
