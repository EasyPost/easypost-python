import easypost

easypost.api_key = 'EASYPOSTAPIRATINGACTIVATEDKEY'

rating = easypost.Rating.create(
  carrier_accounts=["CARRIERACCOUNTID1", "CARRIERACCOUNTID2"],
  to_address={
    "name": 'Dr. Steve Brule',
    "street1": '179 N Harbor Dr',
    "city": 'Redondo Beach',
    "state": 'CA',
    "zip": '90277',
    "country": 'US',
    "phone": '4153334444',
    "email": 'dr_steve_brule@gmail.com'
  },
  from_address={
    "name": 'EasyPost',
    "street1": '417 Montgomery Street',
    "street2": '5th Floor',
    "city": 'San Francisco',
    "state": 'CA',
    "zip": '94104',
    "country": 'US',
    "phone": '4153334444',
    "email": 'support@easypost.com'
  },
  parcels=[{
    "length": 20.2,
    "width": 10.9,
    "height": 5,
    "weight": 65.9
  }]
)
print(rating)