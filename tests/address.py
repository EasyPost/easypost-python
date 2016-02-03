"""
Unit tests related to 'Address' (https://www.easypost.com/docs/api#addresses).
"""
import unittest
import easypost
from constants import API_KEY as api_key


class AddressTests(unittest.TestCase):

    def test_address_creation_verification(self):
        """
        Create an address and then verify some fields to test whether it was created just fine.
        :return:
        """
        address = dict(
            company="EasyPost",
            street1="118 2nd St",
            street2="4th Fl",
            city="San Francisco",
            state="CA",
            zip="94105",
            phone="415-456-7890")
        address = easypost.Address.create(api_key, **address)
        address.verify()
        address = easypost.Address.retrieve(address.id, api_key=api_key)
        assert address.country == 'US'
        assert address.email == None
        assert address.federal_tax_id == None
        assert address.state == 'CA'
        assert address.zip == '94105'

    def test_address_unicode(self):
        """
        Create an address with unicode field and asserting if it was created correctly.
        :return:
        """
        # unicode
        state = u'DELEGACI\xf3N BENITO JU\xe1REZ'

        address = easypost.Address.create(api_key, state=state)

        assert address.state == state

        # bytestring
        address = easypost.Address.create(api_key, state=state.encode('utf-8'))
        assert address.state == state


if __name__ == "__main__":
    unittest.main()
