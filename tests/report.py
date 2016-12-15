import unittest
import easypost
from constants import API_KEY as api_key

easypost.api_key = api_key

class ReportTests(unittest.TestCase):

  def test_report(self):
    report = easypost.Report.create(
        start_date="2012-12-01",
        end_date="2013-01-01",
        type="shipment"
    )

    assert report.object == "ShipmentReport"
    assert report.status == "available"

    report2 = easypost.Report.retrieve(report.id, api_key=api_key)
    assert report2.id == report.id

    reports = easypost.Report.all(api_key=api_key, type = "shipment")
    assert len(reports["reports"])
    assert reports["reports"][0].id == report.id == report2.id
