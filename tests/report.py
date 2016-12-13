import unittest
import easypost
from constants import API_KEY as api_key

easypost.api_key = api_key

class ReportTests(unittest.TestCase):

  def test_report_creation(self):
    report = easypost.Parcel.create(
        start_date="2012-12-01",
        end_date= "2013-01-01",
        type="shipment"
    )

    assert parcel.object == "ShipmentReport"
    assert parcel.status == "available"

