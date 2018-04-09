import easypost
easypost.api_key = 'PRODUCTION API KEY'

me = easypost.User.retrieve()

child_user = easypost.User.create(
    name='Python All-Things-Testing',
    phone_number='555-555-5555'
)
id = child_user.id

retrieved_user = easypost.User.retrieve(id)

new_name = 'Python All-Things-Tested'
retrieved_user.name = new_name
retrieved_user.save()

updated_user = easypost.User.retrieve(id)
