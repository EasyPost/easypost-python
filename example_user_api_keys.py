import easypost
easypost.api_key = 'PRODUCTION API KEY'

# Here are two different ways to retrieve your api_keys
api_keys = easypost.User.all_api_keys()
my_keys1 = api_keys.keys

me = easypost.User.retrieve_me()
my_keys2 = me.api_keys()

# Here is how to retrieve the api_keys of a child user
child = me.children[0]
child_keys = child.api_keys()
