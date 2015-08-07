import sys
from inspect import currentframe, getframeinfo

import easypost
easypost.api_key = 'API KEY'

original_num_cas = len(easypost.CarrierAccount.all())

description = "A test Ups Account"
reference = "PythonClientUpsTestAccount"

created_ca = easypost.CarrierAccount.create(
    type="UpsAccount",
    description=description,
    reference=reference,
    credentials={
         "account_number": "A1A1A1",
         "user_id": "UPSDOTCOM_USERNAME",
         "password": "UPSDOTCOM_PASSWORD",
         "access_license_number": "UPS_ACCESS_LICENSE_NUMBER"})

caid = created_ca["id"]

interm_num_cas = len(easypost.CarrierAccount.all())
if interm_num_cas != original_num_cas + 1:
    print "FAILURE: CarrierAccount not created correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

retrieved_ca = easypost.CarrierAccount.retrieve(caid)
if retrieved_ca["id"] != created_ca["id"]:
    print "FAILURE: CarrierAccount not retrieved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

if retrieved_ca["description"] != description:
    print "FAILURE: CarrierAccount not retrieved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

if retrieved_ca["reference"] != reference:
    print "FAILURE: CarrierAccount not retrieved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)


updated_ca = retrieved_ca
updated_description = "An updated description for a test Ups Account"
updated_account_number = "B2B2B2B2"
retrieved_ca.description = updated_description
retrieved_ca.credentials = {
    "account_number": updated_account_number,
    "user_id": "UPSDOTCOM_USERNAME",
    "password": "UPSDOTCOM_PASSWORD",
    "access_license_number": "UPS_ACCESS_LICENSE_NUMBER"
}
retrieved_ca.save()

updated_ca = easypost.CarrierAccount.retrieve(caid)
if updated_ca["id"] != created_ca["id"]:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

if updated_ca["description"] != updated_description:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

if updated_ca["credentials"]["account_number"] != updated_account_number:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)


reupdated_account_number = "C3C3C3C3C3"
updated_user_id = "A_NEW_UPS_USERNAME"
updated_ca.credentials["account_number"] = reupdated_account_number
updated_ca.credentials["user_id"] = updated_user_id
updated_ca.save()

reupdated_ca = easypost.CarrierAccount.retrieve(caid)
if reupdated_ca["id"] != created_ca["id"]:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

if reupdated_ca["credentials"]["account_number"] != reupdated_account_number:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

if reupdated_ca["credentials"]["user_id"] != updated_user_id:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)


final_ca = reupdated_ca.save()
if final_ca["id"] != created_ca["id"]:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

if final_ca["credentials"]["account_number"] != reupdated_account_number:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)

if final_ca["credentials"]["user_id"] != updated_user_id:
    print "FAILURE: CarrierAccount not saved correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)


final_ca.delete()

final_num_cas = len(easypost.CarrierAccount.all())
if final_num_cas != original_num_cas:
    print "FAILURE: CarrierAccount not deleted correctly"
    frameinfo = getframeinfo(currentframe())
    print frameinfo.filename, frameinfo.lineno
    sys.exit(0)
