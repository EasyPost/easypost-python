import easypost
easypost.api_key = 'rAGbJ5ZEaGQqhBFNzhgVkA'

me = easypost.User.retrieve()

child_user = easypost.User.create(
    name='Python All-Things-Testing',
    password='password1',
    password_confirmation='password1',
    phone_number='7778675309'
)
id = child_user.id

retrieved_user = easypost.User.retrieve(id)

new_name = 'Python All-Things-Tested'
retrieved_user.name = new_name
retrieved_user.save()

updated_user = easypost.User.retrieve(id)
