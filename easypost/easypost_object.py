import json

import easypost


def convert_to_easypost_object(response, api_key, parent=None, name=None):
    """Convert a response to an EasyPost object."""
    types = {
        "Address": easypost.Address,
        "Batch": easypost.Batch,
        "Brand": easypost.Brand,
        "CarrierAccount": easypost.CarrierAccount,
        "CustomsInfo": easypost.CustomsInfo,
        "CustomsItem": easypost.CustomsItem,
        "Event": easypost.Event,
        "Insurance": easypost.Insurance,
        "Order": easypost.Order,
        "Parcel": easypost.Parcel,
        "PaymentLogReport": easypost.Report,
        "Pickup": easypost.Pickup,
        "PickupRate": easypost.PickupRate,
        "PostageLabel": easypost.PostageLabel,
        "Rate": easypost.Rate,
        "Refund": easypost.Refund,
        "RefundReport": easypost.Report,
        "Report": easypost.Report,
        "ScanForm": easypost.ScanForm,
        "Shipment": easypost.Shipment,
        "ShipmentInvoiceReport": easypost.Report,
        "ShipmentReport": easypost.Report,
        "TaxIdentifier": easypost.TaxIdentifier,
        "Tracker": easypost.Tracker,
        "TrackerReport": easypost.Report,
        "User": easypost.User,
        "Webhook": easypost.Webhook,
    }

    prefixes = {
        "adr": easypost.Address,
        "batch": easypost.Batch,
        "ca": easypost.CarrierAccount,
        "cstinfo": easypost.CustomsInfo,
        "cstitem": easypost.CustomsItem,
        "evt": easypost.Event,
        "hook": easypost.Webhook,
        "ins": easypost.Insurance,
        "order": easypost.Order,
        "pickup": easypost.Pickup,
        "pickuprate": easypost.PickupRate,
        "pl": easypost.PostageLabel,
        "plrep": easypost.Report,
        "prcl": easypost.Parcel,
        "rate": easypost.Rate,
        "refrep": easypost.Report,
        "rfnd": easypost.Refund,
        "sf": easypost.ScanForm,
        "shp": easypost.Shipment,
        "shpinvrep": easypost.Report,
        "shprep": easypost.Report,
        "trk": easypost.Tracker,
        "trkrep": easypost.Report,
        "user": easypost.User,
    }

    if isinstance(response, list):
        return [convert_to_easypost_object(r, api_key, parent) for r in response]
    elif isinstance(response, dict):
        response = response.copy()
        cls_name = response.get("object", EasyPostObject)
        cls_id = response.get("id", None)
        if isinstance(cls_name, str):
            cls = types.get(cls_name, EasyPostObject)
        elif cls_id is not None:
            cls = prefixes.get(cls_id[0 : cls_id.find("_")], EasyPostObject)
        else:
            cls = EasyPostObject
        return cls.construct_from(response, api_key, parent, name)
    else:
        return response


class EasyPostObject(object):
    def __init__(self, easypost_id=None, api_key=None, parent=None, name=None, **params):
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

    def __setattr__(self, k, v):
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

    def __getattr__(self, k):
        try:
            return self.__dict__[k]
        except KeyError:
            pass
        raise AttributeError("%r object has no attribute %r" % (type(self).__name__, k))

    def __getitem__(self, k):
        return self.__dict__[k]

    def get(self, k, default=None):
        try:
            return self[k]
        except KeyError:
            return default

    def setdefault(self, k, default=None):
        try:
            return self[k]
        except KeyError:
            self[k] = default
        return default

    def __setitem__(self, k, v):
        setattr(self, k, v)

    def keys(self):
        return self._values.keys()

    def values(self):
        return self._values.keys()

    @classmethod
    def construct_from(cls, values, api_key=None, parent=None, name=None):
        """Construct an object."""
        instance = cls(values.get("id"), api_key, parent, name)
        instance.refresh_from(values, api_key)
        return instance

    def refresh_from(self, values, api_key):
        """Update local object with changes from the API."""
        self._api_key = api_key

        for k, v in sorted(values.items()):
            if k == "id" and self.id != v:
                self.id = v
            if k in self._immutable_values:
                continue
            self.__dict__[k] = convert_to_easypost_object(v, api_key, self, k)
            self._values.add(k)
            self._transient_values.discard(k)
            self._unsaved_values.discard(k)

    def flatten_unsaved(self):
        """Return a dict of `_unsaved_values` values from the current object."""
        values = {}
        for key in self._unsaved_values:
            value = self.get(key)
            if type(value) is EasyPostObject:
                values[key] = value.flatten_unsaved()
            else:
                values[key] = value
        return values

    def __repr__(self):
        type_string = ""

        if isinstance(self.get("object"), str):
            type_string = " %s" % self.get("object").encode("utf8")

        json_string = json.dumps(self.to_dict(), sort_keys=True, indent=2, cls=EasyPostObjectEncoder)

        return "<%s%s at %s> JSON: %s" % (type(self).__name__, type_string, hex(id(self)), json_string)

    def __str__(self):
        return self.to_json(indent=2)

    def __eq__(self, other):
        if not isinstance(other, EasyPostObject):
            return False
        return self.__str__() == other.__str__()

    def to_json(self, indent=None):
        """Convert current object to json string."""
        return json.dumps(self.to_dict(), sort_keys=True, indent=indent, cls=EasyPostObjectEncoder)

    def to_dict(self):
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
    def default(self, obj):
        """Convert easypost object to a dict."""
        if isinstance(obj, EasyPostObject):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)
