"""
Unit test around Parcel endpoint.
"""
import unittest
import easypost
from constants import API_KEY as api_key


class ParcelTests(unittest.TestCase):

    def test_parcel_creation(self):
        """
        Simply create a Parcel and assert on saved data.
        :return:
        """

        parcel = {
            'predefined_package': "RegionalRateBoxA",
            'length': 10.2,
            'width': 7.8,
            'height': 4.3,
            'weight': 21.2
        }
        parcel = easypost.Parcel.create(api_key, **parcel)
        assert parcel.height == 4.3
        assert parcel.width == 7.8
        assert parcel.weight == 21.2
        assert parcel.predefined_package == 'RegionalRateBoxA'
