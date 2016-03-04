import easypost
easypost.api_key = 'cueqNZUb3ldeWTNX7MU3Mel8UXtaAMUi'

try:
    # this request will raise an error
    address = easypost.Address.create(
        verify_strict=["delivery"],
        street1="UNDELIEVRABLE ST",
        city="San Francisco",
        state="CA",
        zip="94105",
        country="US",
        company="EasyPost",
        phone="415-456-7890"
    )
except easypost.Error as e:
    print(e.http_body)
