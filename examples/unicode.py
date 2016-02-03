import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# unicode
state = u'DELEGACI\xf3N BENITO JU\xe1REZ'

address = easypost.Address.create(state=state)

assert address.state == state

# bytestring
address = easypost.Address.create(state=state.encode('utf-8'))
assert address.state == state
