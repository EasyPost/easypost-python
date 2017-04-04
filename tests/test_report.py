# Unit tests related to 'Report's (https://www.easypost.com/docs/api.html#reports).

import easypost


def test_shipment_report():
    def test_shipment_report():
        report = easypost.Report.create(
            type="shipment",
            start_date="2012-12-01",
            end_date="2013-01-01",
        )

        assert report.object == "ShipmentReport"
        assert report.status in ("available", "new")
        assert report.__class__ == easypost.Report

        report2 = easypost.Report.retrieve(report.id, type="shipment")

        assert report2.__class__ == easypost.Report
        assert report2.id == report.id

        reports = easypost.Report.all(type="shipment")
        assert len(reports["reports"])
        assert reports["reports"][0].id == report.id == report2.id
