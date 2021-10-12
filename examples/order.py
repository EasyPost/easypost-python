import easypost

easypost.api_key = "API_KEY"

order = easypost.Order.create(
    to_address={
        "company": "Oakland Dmv Office",
        "name": "Customer",
        "street1": "5300 Claremont Ave",
        "city": "Oakland",
        "state": "CA",
        "zip": "94618",
        "country": "US",
        "phone": "800-777-0133",
    },
    from_address={
        "name": "EasyPost",
        "company": "EasyPost",
        "street1": "164 Townsend St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94107",
        "phone": "415-456-7890",
    },
    shipments=[
        {
            "parcel": easypost.Parcel.create(
                weight=21.2,
                length=12,
                width=12,
                height=3,
            ),
            "options": {"label_format": "PDF"},
        },
        {
            "parcel": easypost.Parcel.create(
                weight=16,
                length=8,
                width=5,
                height=5,
            ),
            "options": {"label_format": "PDF"},
        },
    ],
)

print(order)

order.buy(carrier="USPS", service="Priority")

for shipment in order.shipments:
    # Insure the parcel
    shipment.insure(amount=100)
    print(shipment.postage_label.label_url)
    print(shipment.tracking_code)
