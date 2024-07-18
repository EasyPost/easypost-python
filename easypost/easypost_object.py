from datetime import datetime
from typing import (
    Any,
    Dict,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)


def convert_to_easypost_object(
    response: Dict[str, Any],
    parent: object = None,
    name: Optional[str] = None,
):
    return None


class EphemeralEasyPostObject(BaseModel):
    mode: Optional[str] = Field(None, alias="mode")
    object_type: Optional[str] = Field(None, alias="object")

    def __str__(self):
        return f"<{self.__class__.__name__} object={self.object_type} mode={self.mode}>"


class PaginatedCollection(BaseModel):
    has_more: Optional[bool]


class EasyPostObject(EphemeralEasyPostObject):
    id: Optional[str] = Field(None, alias="id")
    created_at: Optional[datetime] = Field(None, alias="created_at")
    updated_at: Optional[datetime] = Field(None, alias="updated_at")

    @property
    def prefix(self) -> str:
        return self.id.split("_")[0]

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} object={self.object_type} mode={self.mode} id={self.id}>"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, EasyPostObject):
            return False
        return self.__str__() == other.__str__()

    def to_dict(self) -> Dict[str, Any]:
        # TODO: Re-assess
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
