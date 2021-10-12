import easypost

easypost.api_key = "API_KEY"

event = easypost.Event.retrieve("evt_d0f3c9c1cb724d09ad11cfdf241124b8")
# events = easypost.Event.all()

print(event)
