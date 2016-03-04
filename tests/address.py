# Unit tests related to 'Address' (https://www.easypost.com/docs/api#addresses).
import unittest
import easypost
from constants import API_KEY as api_key

easypost.api_key = api_key


class AddressTests(unittest.TestCase):

    def test_address_creation_verification(self):
        # Create an address and then verify some fields to test whether it was created just fine.
        address = easypost.Address.create(
            company='EasyPost',
            street1='118 2nd St',
            street2='4th Fl',
            city='San Francisco',
            state='CA',
            zip='94105',
            phone='415-456-7890'
        )
        address.verify()

        address = easypost.Address.retrieve(address.id)

        assert address.country == 'US'
        assert address.email is None
        assert address.federal_tax_id is None
        assert address.state == 'CA'
        assert address.zip == '94105'

    def test_address_creation_with_verify(self):
        # Create an address with a verify parameter to test that it verifies accurately
        address = easypost.Address.create(
            verify=['delivery'],
            street1='118 2 streat',
            street2='FL 4',
            city='San Francisco',
            state='CA',
            zip='94105',
            country='US',
            company='EasyPost',
            phone='415-456-7890'
        )

        assert address.id is not None
        assert address.street1 == '118 2ND ST FL 4'
        assert address.street2 == ''
        assert address.country == 'US'

    def test_address_creation_with_verify_failure(self):
        # Create an address with a verify parameter to test that it fails elegantly
        address = easypost.Address.create(
            verify=['delivery'],
            street1='UNDELIEVRABLE ST',
            city='San Francisco',
            state='CA',
            zip='94105',
            country='US',
            company='EasyPost',
            phone='415-456-7890'
        )

        assert address.id is not None
        assert address.street1 == 'UNDELIEVRABLE ST'

        assert address.verifications['delivery']['success'] is False
        assert len(address.verifications['delivery']['errors']) == 2
        assert address.verifications['delivery']['errors'][0]['message'] == 'Address not found'
        assert address.verifications['delivery']['errors'][1]['message'] == 'House number is missing'

    def test_address_creation_with_verify_strict_failure(self):
        # Create an address with a verify strict parameter to test that it fails elegantly
        with self.assertRaises(easypost.Error) as context:
            address = easypost.Address.create(
                verify_strict=['delivery'],
                street1='UNDELIEVRABLE ST',
                city='San Francisco',
                state='CA',
                zip='94105',
                country='US',
                company='EasyPost',
                phone='415-456-7890'
            )

        assert context.exception.http_body == '{"error":{' \
            '"code":"ADDRESS.VERIFY.FAILURE",' \
            '"message":"Address not found",' \
            '"errors":[' \
            '{"field":"address","message":"Address not found"},' \
            '{"field":"street1","message":"House number is missing"}' \
            ']}}'

    def test_address_unicode(self):
        # Create an address with unicode field and assert if it was created correctly.
        state = u'DELEGACI\xf3N BENITO JU\xe1REZ'

        address = easypost.Address.create(state=state)
        assert address.state == state

    def test_address_bytestring(self):
        # Create an address with a bytestring field and assert if it was created correctly.
        state = u'DELEGACI\xf3N BENITO JU\xe1REZ'

        address = easypost.Address.create(state=state.encode('utf-8'))
        assert address.state == state


if __name__ == '__main__':
    unittest.main()
