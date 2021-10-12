import easypost

easypost.api_key = "API_KEY"

# this address will not be verified
address = easypost.Address.create(
    verify=["delivery"],
    street1="UNDELIEVRABLE ST",
    city="San Francisco",
    state="CA",
    zip="94105",
    country="US",
    company="EasyPost",
    phone="415-456-7890",
)

print(address.verifications)
