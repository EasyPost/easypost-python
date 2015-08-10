import easypost
easypost.api_key = 'VPxkdfBEY0xvQiy8dJOapw'

original_num_cas = len(easypost.CarrierAccount.all())

created_ca = easypost.CarrierAccount.create(
    type="UpsAccount",
    description="A test Ups Account",
    reference="PythonClientUpsTestAccount",
    credentials={
         "account_number": "A1A1A1",
         "user_id": "UPSDOTCOM_USERNAME",
         "password": "UPSDOTCOM_PASSWORD",
         "access_license_number": "UPS_ACCESS_LICENSE_NUMBER"})

caid = created_ca["id"]

retrieved_ca = easypost.CarrierAccount.retrieve(caid)
retrieved_ca.description = "An updated description for a test Ups Account"
retrieved_ca.credentials = {
    "account_number": "B2B2B2B2",
    "user_id": "UPSDOTCOM_USERNAME",
    "password": "UPSDOTCOM_PASSWORD",
    "access_license_number": "UPS_ACCESS_LICENSE_NUMBER"
}
retrieved_ca.save()

updated_ca = easypost.CarrierAccount.retrieve(caid)
updated_ca.credentials["account_number"] = "C3C3C3C3C3"
updated_ca.credentials["user_id"] = "A_NEW_UPS_USERNAME"
updated_ca.save()

reupdated_ca = easypost.CarrierAccount.retrieve(caid)

# You can call save() with no unsaved changes, but it does nothing
final_ca = reupdated_ca.save()

final_ca.delete()
