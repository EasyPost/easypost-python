Installation
------------------

Required Libraries:
- [Requests](http://docs.python-requests.org/en/latest/) (if not on Google App Engine)

Clone the EasyPost python client repository:

    git clone https://github.com/easypost/easypost-python

Install:
    
    python setup.py install

Import the EasyPost client:

    import easypost

Example
----------------

    import easypost

    easypost.api_key = 'Er1KtysoI4ogfaWswh1v7w'

    to_param = {"street1": "388 Townsend St", "street2": "Apt 20", "city": "San Francisco", "state": "CA", "zip": "94107"}
    from_param = {"street1": "764 Warehouse Ave", "street2": "", "city": "Kansas City", "state": "KS", "zip": "66101"}
    parcel_param = {"predefined_package": "LargeFlatRateBox", "weight": 100.0} // weight in ounces

    to = easypost.Address.create(address=to_param)
    from = easypost.Address.create(address=from_param)

    # CURRENTLY WORKS UP TO HERE!

    parcel = easypost.Parcel.create(address=parcel_param)

    shipment = easypost.Shipment.create(
      to_address = to,
      from_address = from,
      parcel = parcel
    )

    print shipment.rates
    
    shipment.postage_label(shipment.rates[0])
    # alternatively: shipment.postage_label(shipment.lowest_rate())

    print shipment.postage_label.label_url

Documentation
--------------------

Up-to-date documentation at: https://www.geteasypost.com/docs

Tests
--------------------
None yet!