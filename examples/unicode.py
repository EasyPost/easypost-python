import easypost

easypost.api_key = "API_KEY"

# unicode
# TODO: Remove these `fmt` on/off lines once we drop support for Python 2
# fmt: off
state = u"DELEGACI\xf3N BENITO JU\xe1REZ"
# fmt: on

address = easypost.Address.create(state=state)

assert address.state == state

# bytestring
address = easypost.Address.create(state=state.encode("utf-8"))
assert address.state == state
