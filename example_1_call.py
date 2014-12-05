import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# create addresses
to_address = {
    'name': "Sawyer Bateman",
    'street1': "1A Larkspur Cres.",
    'street2': "",
    'city': "St. Albert",
    'state': "AB",
    'zip': "t8n2m4",
    'country': "CA",
    'phone': "780-283-9384"
}

from_address = {
    'name': "Jon Calhoun",
    'street1': "388 Townsend St",
    'city': "San Francisco",
    'state': "CA",
    'zip': "94107",
    'phone': "415-456-7890"
}

parcel = {
    'length': 10.2,
    'width': 7.8,
    'height': 4.3,
    'weight': 21.2
}

customs_item = {
    'description': "EasyPost t-shirts",
    'hs_tariff_number': 123456,
    'origin_country': "US",
    'quantity': 2,
    'value': 96.27,
    'weight': 21.1
}

customs_info = {
    'customs_certify': 1,
    'customs_signer': "Hector Hammerfall",
    'contents_type': "gift",
    'contents_explanation': "",
    'eel_pfc': "NOEEI 30.37(a)",
    'non_delivery_option': "return",
    'restriction_type': "none",
    'restriction_comments': "",
    'customs_items': [customs_item]
}

shipment = easypost.Shipment.create(
    to_address = to_address,
    from_address = from_address,
    parcel = parcel,
    customs_info = customs_info
)

# print shipment.rates
shipment.buy(rate = shipment.lowest_rate())

print(shipment)
