import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# retrieve a shipment by tracking_code
shipment = easypost.Shipment.retrieve("LN123456789US")

print(shipment.id)

shipment.refresh()

print(shipment.id)

print(shipment.label(file_format='PDF'))
