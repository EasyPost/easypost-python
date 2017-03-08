# EasyPost Python Client Library

[![Build Status](https://travis-ci.org/EasyPost/easypost-python.svg?branch=master)](https://travis-ci.org/EasyPost/easypost-python)

EasyPost is the simple shipping API. You can sign up for an account at <https://easypost.com>.

Requirements
------------

* [Python](https://www.python.org) 2.6, 2.7, or 3.3+ (or corresponding [PyPy](https://pypy.org) versions).
* [requests](http://docs.python-requests.org/en/latest/) (if not on Google App Engine)
* [six](https://pythonhosted.org/six/)


Looking for a client library for another language? Check out <https://www.easypost.com/docs/libraries>.


Installation
------------

You can install easypost via pip with:

```bash
pip install easypost
```

Alternatively, you can clone the EasyPost python client repository:

```bash
git clone https://github.com/EasyPost/easypost-python
```

Install:

```bash
python setup.py install
```

Import the EasyPost client:

```python
import easypost
```

Example
-------

```python
import easypost
easypost.api_key = '<YOUR API KEY FROM https://www.easypost.com/account/api-keys>'

# create and verify addresses
to_address = easypost.Address.create(
    verify=["delivery"],
    name = "Dr. Steve Brule",
    street1 = "179 N Harbor Dr",
    street2 = "",
    city = "Redondo Beach",
    state = "CA",
    zip = "90277",
    country = "US",
    phone = "310-808-5243"
)
from_address = easypost.Address.create(
    verify=["delivery"],
    name = "EasyPost",
    street1 = "118 2nd Street",
    street2 = "4th Floor",
    city = "San Francisco",
    state = "CA",
    zip = "94105",
    country = "US",
    phone = "415-456-7890"
)

# create parcel
try:
    parcel = easypost.Parcel.create(
        predefined_package = "Parcel",
        weight = 21.2
    )
except easypost.Error as e:
    print(str(e))
    if e.param is not None:
        print('Specifically an invalid param: %r' % e.param)

parcel = easypost.Parcel.create(
    length = 10.2,
    width = 7.8,
    height = 4.3,
    weight = 21.2
)

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
    from_address = from_address,
    parcel = parcel,
    customs_info = customs_info
)

# buy postage label with one of the rate objects
shipment.buy(rate = shipment.rates[0])
# alternatively: shipment.buy(rate = shipment.lowest_rate())

print(shipment.tracking_code)
print(shipment.postage_label.label_url)

# Insure the shipment for the value
shipment.insure(amount=100)

print(shipment.insurance)
```

Documentation
-------------

Up-to-date documentation is available at: <https://www.easypost.com/docs>


Client Library Development
-------------------------

### Releasing

   1. Add new features to [CHANGELOG.md](CHANGELOG.md)
   1. Bump the version in `VERSION`
   1. Create a git tag
   1. Push to PyPI with `python setup.py sdist upload`

### Running Tests

To run tests:

   - Create a virtualenv for your version of Python (e.g., `python2.7 -m virtualenv venv`)
   - Install dependencies in that virtualenv (`./venv/bin/pip install requests six`)
   - Install test dependencies (`./venv/bin/pip install -r requirements-tests.txt`)
   - Run the tests with `py.test` (`./venv/bin/py.test -vs tests`)
