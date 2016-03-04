import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# this address will be verified
address = easypost.Address.create(
    verify=["delivery"],
    street1="118 2 streat",
    street2="FL 4",
    city="San Francisco",
    state="CA",
    zip="94105",
    country="US",
    company="EasyPost",
    phone="415-456-7890"
)

print(address.street1)
