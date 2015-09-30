# EasyPost Python Client Library

EasyPost is a simple shipping API. You can sign up for an account at https://easypost.com

Requirements
------------

* [Requests](http://docs.python-requests.org/en/latest/) (if not on Google App Engine)

Installation
------------

You can install easypost via pip with:

    pip install easypost

Alternatively, you can clone the EasyPost python client repository:

    git clone https://github.com/EasyPost/easypost-python

Install:
    
    python setup.py install

Import the EasyPost client:

    import easypost

Example
-------

```python
import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# create addresses
to_address = easypost.Address.create(
  name = "Dr. Steve Brule",
  street1 = "179 N Harbor Dr",
  street2 = "",
  city = "Redondo Beach",
  state = "CA",
  zip = "90277",
  country = "US"
)
from_address = easypost.Address.create(
  name = "EasyPost",
  street1 = "118 2nd Street",
  street2 = "4th Floor",
  city = "San Francisco",
  state = "CA",
  zip = "94105",
  phone = "415-456-7890"
)

# verify address
try:
  verified_from_address = from_address.verify()
except easypost.Error as e:
  raise e
if hasattr(verified_from_address, 'message'):
  # the from address is not invalid, but it has an issue
  pass

# create parcel
try:
  parcel = easypost.Parcel.create(
    predefined_package = "Parcel",
    weight = 21.2
  )
except easypost.Error as e:
  print e.message
  if e.param != None:
    print 'Specifically an invalid param: ' + e.param

try:
  parcel = easypost.Parcel.create(
    length = 10.2,
    width = 7.8,
    height = 4.3,
    weight = 21.2
  )
except easypost.Error as e:
  raise e

# create customs_info form for intl shipping
customs_item = easypost.CustomsItem.create(
  description = "EasyPost t-shirts",
  hs_tariff_number = 123456,
  origin_country = "US",
  quantity = 2,
  value = 96.27,
  weight = 21.1
)
customs_info = easypost.CustomsInfo.create(
  customs_certify = 1,
  customs_signer = "Hector Hammerfall",
  contents_type = "gift",
  contents_explanation = "",
  eel_pfc = "NOEEI 30.37(a)",
  non_delivery_option = "return",
  restriction_type = "none",
  restriction_comments = "",
  customs_items = [customs_item]
)

# create shipment
shipment = easypost.Shipment.create(
  to_address = to_address,
  from_address = verified_from_address,
  parcel = parcel,
  customs_info = customs_info
)

# buy postage label with one of the rate objects
shipment.buy(rate = shipment.rates[0])
# alternatively: shipment.buy(rate = shipment.lowest_rate())

print shipment.tracking_code
print shipment.postage_label.label_url
```

Documentation
-------------

Up-to-date documentation at: https://www.easypost.com/docs

Tests
-----
Coming soon!
