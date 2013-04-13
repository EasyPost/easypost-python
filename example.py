import easypost

easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

to_address_param = {
  "name": "The Saw",
  "street1": "388 Townsend St",
  "street2": "Apt 30",
  "city": "San Francisco",
  "state": "CA",
  "zip": "94107"
}

resp = easypost.Address.create(address=to_address_param)

print 'Success: %r' % (resp)
