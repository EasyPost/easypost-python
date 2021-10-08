from __future__ import print_function

import easypost

easypost.api_key = "PRODUCTION API KEY"

types = easypost.CarrierAccount.types()

for carrier_type in types:
    print(carrier_type.type)
