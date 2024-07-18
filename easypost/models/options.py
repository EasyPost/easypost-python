from datetime import datetime
from typing import (
    Dict,
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class Options(EasyPostObject):
    additional_handling: Optional[bool] = Field(None, alias="additional_handling")
    address_validation_level: Optional[str] = Field(None, alias="address_validation_level")
    alcohol: Optional[bool] = Field(None, alias="alcohol")
    billing_ref: Optional[str] = Field(None, alias="billing_ref")
    bill_receiver_account: Optional[str] = Field(None, alias="bill_receiver_account")  # Obsolete. Use Payment instead.
    bill_receiver_postal_code: Optional[str] = Field(
        None, alias="bill_receiver_postal_code"
    )  # Obsolete. Use Payment instead.
    bill_third_party_account: Optional[str] = Field(
        None, alias="bill_third_party_account"
    )  # Obsolete. Use Payment instead.
    bill_third_party_country: Optional[str] = Field(
        None, alias="bill_third_party_country"
    )  # Obsolete. Use Payment instead.
    bill_third_party_postal_code: Optional[str] = Field(
        None, alias="bill_third_party_postal_code"
    )  # Obsolete. Use Payment instead.
    by_drone: Optional[bool] = Field(None, alias="by_drone")
    carrier_insurance_amount: Optional[str] = Field(None, alias="carrier_insurance_amount")
    carrier_notification_email: Optional[str] = Field(None, alias="carrier_notification_email")
    carrier_notification_sms: Optional[str] = Field(None, alias="carrier_notification_sms")
    certified_mail: Optional[bool] = Field(None, alias="certified_mail")
    cod_address_id: Optional[str] = Field(None, alias="cod_address_id")
    cod_amount: Optional[str] = Field(None, alias="cod_amount")
    cod_method: Optional[str] = Field(None, alias="cod_method")
    commercial_invoice_format: Optional[str] = Field(None, alias="commercial_invoice_format")
    commercial_invoice_letterhead: Optional[str] = Field(None, alias="commercial_invoice_letterhead")
    commercial_invoice_signature: Optional[str] = Field(None, alias="commercial_invoice_signature")
    commercial_invoice_size: Optional[str] = Field(None, alias="commercial_invoice_size")
    content_description: Optional[str] = Field(None, alias="content_description")
    cost_center: Optional[str] = Field(None, alias="cost_center")
    currency: Optional[str] = Field(None, alias="currency")
    customs_broker_address_id: Optional[str] = Field(None, alias="customs_broker_address_id")
    customs_include_shipping: Optional[str] = Field(None, alias="customs_include_shipping")
    declared_value: Optional[float] = Field(None, alias="declared_value")
    delivered_duty_paid: Optional[bool] = Field(None, alias="delivered_duty_paid")
    delivery_confirmation: Optional[str] = Field(None, alias="delivery_confirmation")
    delivery_time_preference: Optional[str] = Field(None, alias="delivery_time_preference")
    delivery_min_datetime: Optional[str] = Field(None, alias="delivery_min_datetime")
    delivery_max_datetime: Optional[str] = Field(None, alias="delivery_max_datetime")
    dropoff_max_datetime: Optional[datetime] = Field(None, alias="dropoff_max_datetime")
    dropoff_type: Optional[str] = Field(None, alias="dropoff_type")
    dry_ice: Optional[bool] = Field(None, alias="dry_ice")
    dry_ice_medical: Optional[str] = Field(None, alias="dry_ice_medical")
    dry_ice_weight: Optional[str] = Field(None, alias="dry_ice_weight")
    duty_payment: Optional[Dict[str, object]] = Field(None, alias="duty_payment")
    duty_payment_account: Optional[str] = Field(None, alias="duty_payment_account")
    endorsement: Optional[str] = Field(None, alias="endorsement")
    end_shipper_id: Optional[str] = Field(None, alias="end_shipper_id")
    freight_charge: Optional[str] = Field(None, alias="freight_charge")
    group: Optional[str] = Field(None, alias="group")
    handling_instructions: Optional[str] = Field(None, alias="handling_instructions")
    hazmat: Optional[str] = Field(None, alias="hazmat")
    hold_for_pickup: Optional[bool] = Field(None, alias="hold_for_pickup")
    image_format: Optional[str] = Field(None, alias="image_format")
    importer_address_id: Optional[str] = Field(None, alias="importer_address_id")
    import_federal_tax_id: Optional[str] = Field(None, alias="import_federal_tax_id")
    import_state_tax_id: Optional[str] = Field(None, alias="import_state_tax_id")
    incoterm: Optional[str] = Field(None, alias="incoterm")
    invoice_number: Optional[str] = Field(None, alias="invoice_number")
    label_date: Optional[datetime] = Field(None, alias="label_date")
    label_format: Optional[str] = Field(None, alias="label_format")
    label_size: Optional[str] = Field(None, alias="label_size")
    license_number: Optional[str] = Field(None, alias="license_number")
    machinable: Optional[str] = Field(None, alias="machinable")
    neutral_delivery: Optional[bool] = Field(None, alias="neutral_delivery")
    non_contract: Optional[bool] = Field(None, alias="non_contract")
    overlabel_construct_code: Optional[str] = Field(None, alias="overlabel_construct_code")
    overlabel_original_tracking_number: Optional[str] = Field(None, alias="overlabel_original_tracking_number")
    parties_to_transaction_are_related: Optional[str] = Field(None, alias="parties_to_transaction_are_related")
    payment: Optional[Dict[str, object]] = Field(None, alias="payment")
    peel_and_return: Optional[bool] = Field(None, alias="peel_and_return")
    pickup_max_datetime: Optional[datetime] = Field(None, alias="pickup_max_datetime")
    pickup_min_datetime: Optional[datetime] = Field(None, alias="pickup_min_datetime")
    po_sort: Optional[str] = Field(None, alias="po_sort")
    postage_label_inline: Optional[bool] = Field(None, alias="postage_label_inline")
    print_custom: Optional[List[Dict[str, object]]] = Field(None, alias="print_custom")
    print_custom_1: Optional[str] = Field(None, alias="print_custom_1")
    print_custom_1_barcode: Optional[bool] = Field(None, alias="print_custom_1_barcode")
    print_custom_1_code: Optional[str] = Field(None, alias="print_custom_1_code")
    print_custom_2: Optional[str] = Field(None, alias="print_custom_2")
    print_custom_2_barcode: Optional[bool] = Field(None, alias="print_custom_2_barcode")
    print_custom_2_code: Optional[str] = Field(None, alias="print_custom_2_code")
    print_custom_3: Optional[str] = Field(None, alias="print_custom_3")
    print_custom_3_barcode: Optional[bool] = Field(None, alias="print_custom_3_barcode")
    print_custom_3_code: Optional[str] = Field(None, alias="print_custom_3_code")
    print_rate: Optional[bool] = Field(None, alias="print_rate")
    receiver_liquor_license: Optional[str] = Field(None, alias="receiver_liquor_license")
    registered_mail: Optional[bool] = Field(None, alias="registered_mail")
    registered_mail_amount: Optional[float] = Field(None, alias="registered_mail_amount")
    return_receipt: Optional[bool] = Field(None, alias="return_receipt")
    return_service: Optional[str] = Field(None, alias="return_service")
    saturday_delivery: Optional[bool] = Field(None, alias="saturday_delivery")
    settlement_method: Optional[str] = Field(None, alias="settlement_method")
    smartpost_hub: Optional[str] = Field(None, alias="smartpost_hub")
    smartpost_manifest: Optional[str] = Field(None, alias="smartpost_manifest")
    special_rates_eligibility: Optional[str] = Field(None, alias="special_rates_eligibility")
    suppress_etd: Optional[bool] = Field(None, alias="suppress_etd")
    tax_id_expiration_date: Optional[str] = Field(None, alias="tax_id_expiration_date")
