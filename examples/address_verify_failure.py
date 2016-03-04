import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# this address will not be verified
address = easypost.Address.create(
    verify=["delivery"],
    street1="UNDELIEVRABLE ST",
    city="San Francisco",
    state="CA",
    zip="94105",
    country="US",
    company="EasyPost",
    phone="415-456-7890"
)

print(address.verifications)
