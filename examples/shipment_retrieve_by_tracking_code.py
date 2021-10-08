import easypost

easypost.api_key = "API_KEY"

# retrieve a shipment by tracking_code
shipment = easypost.Shipment.retrieve("LN123456789US")

print(shipment.id)

shipment.refresh()

print(shipment.id)

print(shipment.label(file_format="PDF"))
