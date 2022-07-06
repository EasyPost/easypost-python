import easypost.beta
from easypost.address import Address
from easypost.batch import Batch
from easypost.billing import Billing
from easypost.brand import Brand
from easypost.carrier_account import CarrierAccount
from easypost.customs_info import CustomsInfo
from easypost.customs_item import CustomsItem
from easypost.error import Error
from easypost.event import Event
from easypost.insurance import Insurance
from easypost.order import Order
from easypost.parcel import Parcel
from easypost.pickup import Pickup
from easypost.pickup_rate import PickupRate
from easypost.postage_label import PostageLabel
from easypost.rate import Rate
from easypost.refund import Refund
from easypost.report import Report
from easypost.scanform import ScanForm
from easypost.shipment import Shipment
from easypost.tax_identifier import TaxIdentifier
from easypost.tracker import Tracker
from easypost.user import User
from easypost.webhook import Webhook

from .version import (
    VERSION,
    VERSION_INFO,
)


__author__ = "EasyPost <oss@easypost.com>"
__version__ = VERSION
version_info = VERSION_INFO

# config
api_key = None
api_base = "https://api.easypost.com/v2"
