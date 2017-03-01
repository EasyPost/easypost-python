# Unit tests related to 'Users' (https://www.easypost.com/docs/api#users).
import unittest
import easypost
from . import constants


class UserTests(unittest.TestCase):

    def test_child_user_create(self):
        easypost.api_key = constants.PROD_API_KEY  # Use a Prod key for this test

        # Create an address and then verify some fields to test whether it was created just fine.
        child_user = easypost.User.create(
            name='Python All-Things-Testing',
            password='password1',
            password_confirmation='password1',
        )
        child_id = child_user.id
        assert child_id is not None

        retrieved_user = easypost.User.retrieve(child_id)
        assert retrieved_user.id == child_id
        assert retrieved_user.name == 'Python All-Things-Testing'

        new_name = 'Python All-Things-Tested'
        retrieved_user.name = new_name
        retrieved_user.save()

        updated_user = easypost.User.retrieve(child_id)
        assert updated_user.id == child_id
        assert updated_user.name == 'Python All-Things-Tested'

        easypost.api_key = constants.API_KEY  # Reset the api_key at the end, just in case
