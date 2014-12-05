import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'
# easypost.api_base = 'http://localhost:5000/v2'

# create addresses
to_address = easypost.Address.create(
    name = "Sawyer Bateman",
    street1 = "1A Larkspur Cres.",
    street2 = "",
    city = "St. Albert",
    state = "AB",
    zip = "t8n2m4",
    country = "CA",
    phone = "780-283-9384"
)
from_address = easypost.Address.create(
    name = "Jon Calhoun",
    street1 = "388 Townsend St",
    city = "San Francisco",
    state = "CA",
    zip = "94107",
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
        predefined_package = "InvalidPackageName",
        weight = 21.2
    )
except easypost.Error as e:
    print(e.message)
    if e.param != None:
        print('Specifically an invalid param: ' + e.param)

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
# shipment.buy(rate = shipment.rates[0])
# shipment.buy(rate = shipment.lowest_rate('usps'))
shipment.buy(rate = shipment.lowest_rate(['USPS', 'ups'], 'priorityMAILInternational'))

# shipment.refund()
# print(shipment.refund_status)

print(shipment.tracking_code)
print(shipment.postage_label.label_url)
