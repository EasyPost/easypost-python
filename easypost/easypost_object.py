import importlib
import json
import re
from typing import (
    Any,
    Optional,
)

from easypost.constant import NO_ATTRIBUTE_ERROR


EASYPOST_OBJECT_ID_PREFIX_TO_CLASS_NAME_MAP: dict[str, Any] = {
    "adr": "Address",
    "ak": "ApiKey",
    "batch": "Batch",
    "brd": "Brand",
    "ca": "CarrierAccount",
    "cfrep": "Report",
    "clm": "Claim",
    "cstinfo": "CustomsInfo",
    "cstitem": "CustomsItem",
    "es": "EndShipper",
    "evt": "Event",
    "hook": "Webhook",
    "ins": "Insurance",
    "order": "Order",
    "payload": "Payload",
    "pickup": "Pickup",
    "pickuprate": "PickupRate",
    "pl": "PostageLabel",
    "plrep": "Report",
    "prcl": "Parcel",
    "rate": "Rate",
    "refrep": "Report",
    "rfnd": "Refund",
    "sf": "ScanForm",
    "shp": "Shipment",
    "shpinvrep": "Report",
    "shprep": "Report",
    "trk": "Tracker",
    "trkrep": "Report",
    "user": "User",
}

OBJECT_CLASS_NAME_OVERRIDES: dict[str, Any] = {
    "CashFlowReport": "Report",
    "PaymentLogReport": "Report",
    "RefundReport": "Report",
    "ShipmentInvoiceReport": "Report",
    "ShipmentReport": "Report",
    "TrackerReport": "Report",
}


def convert_to_easypost_object(
    response: dict[str, Any],
    parent: object = None,
    name: Optional[str] = None,
):
    """Convert a response to an EasyPostObject."""
    if isinstance(response, list):
        return [convert_to_easypost_object(response=item, parent=parent) for item in response]
    elif isinstance(response, dict):
        object_type_str = response.get("object", EasyPostObject)
        class_name = OBJECT_CLASS_NAME_OVERRIDES.get(object_type_str, EasyPostObject)
        object_id = response.get("id")

        if object_id is not None:
            # If an object ID is present, use it to find the class type instead.
            object_id_prefix = object_id.split("_")[0]
            class_name = EASYPOST_OBJECT_ID_PREFIX_TO_CLASS_NAME_MAP.get(object_id_prefix, EasyPostObject)

        # Dynamically import class models due to circular imports of EasyPostObject
        class_model = (
            getattr(
                importlib.import_module(f'easypost.models.{re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()}'),
                class_name,
            )
            if class_name != EasyPostObject
            else EasyPostObject
        )

        obj = class_model.construct_from(values=response, parent=parent, name=name)

        return obj
    else:
        return response


class EasyPostObject(object):
    def __init__(
        self,
        id: Optional[str] = None,
        parent: Optional[object] = None,
        name: Optional[str] = None,
        **params,
    ):
        self.__dict__["_values"] = set()
        self.__dict__["_immutable_values"] = {"id"}
        self.__dict__["_parent"] = parent
        self.__dict__["_name"] = name

        if id:
            self.id = id

    def __setattr__(self, k, v: Any) -> None:
        self.__dict__[k] = v

        if k not in self._immutable_values:
            self._values.add(k)
            self._unsaved_values.add(k)
            cur = self
            cur_parent = self._parent

            while cur_parent:
                if cur._name:
                    cur_parent._unsaved_values.add(cur._name)
                cur = cur_parent
                cur_parent = cur._parent

    def __getattr__(self, k) -> Any:
        try:
            return self.__dict__[k]
        except KeyError:
            pass
        raise AttributeError(NO_ATTRIBUTE_ERROR.format(type(self).__name__, k))

    def __getitem__(self, k):
        return self.__dict__[k]

    def get(self, k, default: Any = None) -> Any:
        try:
            return self[k]
        except KeyError:
            return default

    def setdefault(self, k, default: Any = None) -> Any:
        try:
            return self[k]
        except KeyError:
            self[k] = default
        return default

    def __setitem__(self, k, v) -> None:
        setattr(self, k, v)

    @property
    def keys(self) -> list[str]:
        return self._values.keys()

    @property
    def values(self) -> list[Any]:
        return self._values.keys()

    @classmethod
    def construct_from(
        cls,
        values: dict[str, Any],
        parent: object = None,
        name: Optional[str] = None,
    ) -> object:
        """Construct an EasyPostObject from values returned by the API."""
        instance = cls(id=values.get("id"), parent=parent, name=name)
        instance.convert_each_value(values=values)

        return instance

    def convert_each_value(self, values: dict[str, Any]) -> None:
        """Convert each value of a response into an EasyPostObject."""
        for k, v in sorted(values.items()):
            if k == "id" and self.id != v:
                self.id = v
            if k in self._immutable_values:
                continue
            self.__dict__[k] = convert_to_easypost_object(response=v, parent=self, name=k)
            self._values.add(k)

    def __repr__(self) -> str:
        """String representation of an EasyPostObject."""
        type_string = ""

        if isinstance(self.get("object"), str):
            type_string = " %s" % self.get("object").encode("utf8")

        json_string = json.dumps(obj=self.to_dict(), sort_keys=True, indent=2, cls=EasyPostObjectEncoder)

        return "<%s%s at %s> JSON: %s" % (
            type(self).__name__,
            type_string,
            hex(id(self)),
            json_string,
        )

    def __str__(self) -> str:
        return self.to_json(indent=2)

    def __eq__(self, other) -> bool:
        if not isinstance(other, EasyPostObject):
            return False
        return self.__str__() == other.__str__()

    def to_json(self, indent: Optional[int] = None) -> str:
        """Convert current object to json string."""
        return json.dumps(obj=self.to_dict(), sort_keys=True, indent=indent, cls=EasyPostObjectEncoder)

    def to_dict(self) -> dict[str, Any]:
        """Convert current object to a dict."""

        def _serialize(o):
            if isinstance(o, EasyPostObject):
                return o.to_dict()
            if isinstance(o, list):
                return [_serialize(r) for r in o]
            return o

        d = {"id": self.get("id")} if self.get("id") else {}
        for k in sorted(self._values):
            v = getattr(self, k)
            v = _serialize(v)
            d[k] = v
        return d


class EasyPostObjectEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        """Convert an EasyPostObject to a dict."""
        if isinstance(obj, EasyPostObject):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, o=obj)
