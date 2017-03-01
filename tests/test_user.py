# Unit tests related to 'Users' (https://www.easypost.com/docs/api#users).

import easypost


def test_child_user_create(prod_api_key):
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
