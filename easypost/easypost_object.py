import json
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import easypost


EASYPOST_OBJECT_ID_PREFIX_TO_CLASS_NAME_MAP = {
    "adr": "Address",
    "batch": "Batch",
    "brd": "Brand",
    "ca": "CarrierAccount",
    "cfrep": "Report",
    "cstinfo": "CustomsInfo",
    "cstitem": "CustomsItem",
    "evt": "Event",
    "hook": "Webhook",
    "ins": "Insurance",
    "order": "Order",
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

OBJECT_CLASS_NAME_OVERRIDES = {
    "CashFlowReport": "Report",
    "PaymentLogReport": "Report",
    "RefundReport": "Report",
    "ShipmentInvoiceReport": "Report",
    "ShipmentReport": "Report",
    "TrackerReport": "Report",
}


def convert_to_easypost_object(
    response: Dict[str, Any],
    api_key: Optional[str] = None,
    parent: object = None,
    name: Optional[str] = None,
):
    """Convert a response to an EasyPost object."""
    if isinstance(response, list):
        return [convert_to_easypost_object(response=item, api_key=api_key, parent=parent) for item in response]
    elif isinstance(response, dict):
        response = response.copy()
        object_type_str = response.get("object", "EasyPostObject")
        class_name = OBJECT_CLASS_NAME_OVERRIDES.get(object_type_str, object_type_str)

        object_id = response.get("id", None)
        if object_id is not None:
            # If an object ID is present, use it to find the class type instead.
            object_id_prefix = object_id.split("_")[0]
            class_name = EASYPOST_OBJECT_ID_PREFIX_TO_CLASS_NAME_MAP.get(object_id_prefix, "EasyPostObject")

        cls = getattr(easypost, class_name, EasyPostObject)
        obj = cls.construct_from(values=response, api_key=api_key, parent=parent, name=name)
        return obj
    else:
        return response


class EasyPostObject(object):
    def __init__(
        self,
        easypost_id: Optional[str] = None,
        api_key: Optional[str] = None,
        parent: object = None,
        name: Optional[str] = None,
        **params,
    ):
        self.__dict__["_values"] = set()
        self.__dict__["_unsaved_values"] = set()
        self.__dict__["_transient_values"] = set()
        self.__dict__["_immutable_values"] = {"_api_key", "id"}
        self.__dict__["_retrieve_params"] = params

        self.__dict__["_parent"] = parent
        self.__dict__["_name"] = name

        self.__dict__["_api_key"] = api_key

        if easypost_id:
            self.id = easypost_id

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
        raise AttributeError("%r object has no attribute %r" % (type(self).__name__, k))

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
    def keys(self) -> List[str]:
        return self._values.keys()

    @property
    def values(self) -> List[Any]:
        return self._values.keys()

    @classmethod
    def construct_from(
        cls,
        values: Dict[str, Any],
        api_key: Optional[str] = None,
        parent: object = None,
        name: Optional[str] = None,
    ) -> object:
        """Construct an object."""
        instance = cls(easypost_id=values.get("id"), api_key=api_key, parent=parent, name=name)
        instance.refresh_from(values=values, api_key=api_key)
        return instance

    def refresh_from(self, values: Dict[str, Any], api_key: Optional[str] = None) -> None:
        """Update local object with changes from the API."""
        self._api_key = api_key

        for k, v in sorted(values.items()):
            if k == "id" and self.id != v:
                self.id = v
            if k in self._immutable_values:
                continue
            self.__dict__[k] = convert_to_easypost_object(response=v, api_key=api_key, parent=self, name=k)
            self._values.add(k)
            self._transient_values.discard(k)
            self._unsaved_values.discard(k)

    def flatten_unsaved(self) -> Dict[str, Any]:
        """Return a dict of `_unsaved_values` values from the current object."""
        values = {}
        for key in self._unsaved_values:
            value = self.get(key)
            if type(value) is EasyPostObject:
                values[key] = value.flatten_unsaved()
            else:
                values[key] = value
        return values

    def __repr__(self) -> str:
        type_string = ""

        if isinstance(self.get("object"), str):
            type_string = " %s" % self.get("object").encode("utf8")

        json_string = json.dumps(obj=self.to_dict(), sort_keys=True, indent=2, cls=EasyPostObjectEncoder)

        return "<%s%s at %s> JSON: %s" % (type(self).__name__, type_string, hex(id(self)), json_string)

    def __str__(self) -> str:
        return self.to_json(indent=2)

    def __eq__(self, other) -> bool:
        if not isinstance(other, EasyPostObject):
            return False
        return self.__str__() == other.__str__()

    def to_json(self, indent: int = None) -> str:
        """Convert current object to json string."""
        return json.dumps(obj=self.to_dict(), sort_keys=True, indent=indent, cls=EasyPostObjectEncoder)

    def to_dict(self) -> Dict[str, Any]:
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
        """Convert easypost object to a dict."""
        if isinstance(obj, EasyPostObject):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, o=obj)
