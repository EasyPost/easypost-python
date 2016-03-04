import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

# create address
address = easypost.Address.create(
    company="EasyPost",
    street1="118 2nd St",
    street2="4th Fl",
    city="San Francisco",
    state="CA",
    zip="94105",
    phone="415-456-7890"
)

verified_address = address.verify()

print(verified_address)
