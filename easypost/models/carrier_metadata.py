import enum
from typing import (
    List,
    Optional,
)

from easypost.easypost_object import EasyPostObject
from pydantic import Field


class CarrierMetadataType(enum.Enum):
    ServiceLevels = "service_levels"
    PredefinedPackages = "predefined_packages"
    ShipmentOptions = "shipment_options"
    SupportedFeatures = "supported_features"


class PredefinedPackage(EasyPostObject):
    carrier: Optional[str] = Field(None, alias="carrier")
    description: Optional[str] = Field(None, alias="description")
    dimensions: Optional[List[str]] = Field(None, alias="dimensions")
    human_readable: Optional[str] = Field(None, alias="human_readable")
    max_weight: Optional[str] = Field(None, alias="max_weight")
    name: Optional[str] = Field(None, alias="name")


class ServiceLevel(EasyPostObject):
    carrier: Optional[str] = Field(None, alias="carrier")
    description: Optional[str] = Field(None, alias="description")
    dimensions: Optional[List[str]] = Field(None, alias="dimensions")
    human_readable: Optional[str] = Field(None, alias="human_readable")
    max_weight: Optional[str] = Field(None, alias="max_weight")
    name: Optional[str] = Field(None, alias="name")


class ShipmentOption(EasyPostObject):
    carrier: Optional[str] = Field(None, alias="carrier")
    deprecated: Optional[bool] = Field(None, alias="deprecated")
    description: Optional[str] = Field(None, alias="description")
    human_readable: Optional[str] = Field(None, alias="human_readable")
    name: Optional[str] = Field(None, alias="name")
    type: Optional[str] = Field(None, alias="type")


class SupportedFeature(EasyPostObject):
    carrier: Optional[str] = Field(None, alias="carrier")
    description: Optional[str] = Field(None, alias="description")
    name: Optional[str] = Field(None, alias="name")
    supported: Optional[bool] = Field(None, alias="supported")


class Carrier(EasyPostObject):
    name: Optional[str] = Field(None, alias="name")
    human_readable: Optional[str] = Field(None, alias="human_readable")
    predefined_packages: Optional[List[PredefinedPackage]] = Field(None, alias="predefined_packages")
    service_levels: Optional[List[ServiceLevel]] = Field(None, alias="service_levels")
    shipment_options: Optional[List[ShipmentOption]] = Field(None, alias="shipment_options")
    supported_features: Optional[List[SupportedFeature]] = Field(None, alias="supported_features")


class CarrierMetadata(EasyPostObject):
    carriers: Optional[List[Carrier]] = Field(None, alias="carriers")
