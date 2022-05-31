import re
from typing import (
    Any,
    List,
    Optional,
)

from easypost.easypost_object import (
    EasyPostObject,
    convert_to_easypost_object,
)
from easypost.error import Error
from easypost.requestor import (
    RequestMethod,
    Requestor,
)


class Resource(EasyPostObject):
    def _ident(self) -> List[str]:
        return [self.get("id")]

    @classmethod
    def retrieve(cls, easypost_id: str, api_key: Optional[str] = None, **params) -> object:
        """Retrieve an object from the EasyPost API."""
        instance = cls(easypost_id=easypost_id, api_key=api_key, **params)
        instance.refresh()
        return instance

    def refresh(self) -> object:
        """Refresh the local object from the API response."""
        requestor = Requestor(local_api_key=self._api_key)
        url = self.instance_url()
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=self._retrieve_params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    @classmethod
    def snakecase_name(cls) -> str:
        """Return the class name as snake_case."""
        snake_name = (cls.__name__[0:1] + re.sub(r"([A-Z])", r"_\1", cls.__name__[1:])).lower()
        return snake_name

    @classmethod
    def class_url(cls) -> str:
        """Generate a URL based on class name."""
        cls_name = cls.snakecase_name()
        if cls_name[-1:] in ("s", "h"):
            return "/%ses" % cls_name
        else:
            return "/%ss" % cls_name

    def instance_url(self) -> str:
        """Generate an instance URL based on the ID of the object."""
        easypost_id = self.get("id")
        if not easypost_id:
            raise Error("%s instance has invalid ID: %r" % (type(self).__name__, easypost_id))
        return "%s/%s" % (self.class_url(), easypost_id)


class AllResource(Resource):
    @classmethod
    def all(cls, api_key: Optional[str] = None, **params) -> List[Any]:
        """Retrieve a list of records from the API."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()
        response, api_key = requestor.request(method=RequestMethod.GET, url=url, params=params)
        return convert_to_easypost_object(response=response, api_key=api_key)


class CreateResource(Resource):
    @classmethod
    def create(cls, api_key: Optional[str] = None, **params) -> Any:
        """Create an EasyPost object."""
        requestor = Requestor(local_api_key=api_key)
        url = cls.class_url()
        wrapped_params = {cls.snakecase_name(): params}
        response, api_key = requestor.request(method=RequestMethod.POST, url=url, params=wrapped_params)
        return convert_to_easypost_object(response=response, api_key=api_key)


class UpdateResource(Resource):
    def save(self) -> Any:
        """Update an EasyPost object."""
        if self._unsaved_values:
            requestor = Requestor(local_api_key=self._api_key)
            params = {}
            for k in self._unsaved_values:
                params[k] = getattr(self, k)
                if type(params[k]) is EasyPostObject:
                    params[k] = params[k].flatten_unsaved()
            params = {self.snakecase_name(): params}
            url = self.instance_url()
            response, api_key = requestor.request(method=RequestMethod.PATCH, url=url, params=params)
            self.refresh_from(values=response, api_key=api_key)

        return self


class DeleteResource(Resource):
    def delete(self, **params) -> Any:
        """Delete an EasyPost object."""
        requestor = Requestor(local_api_key=self._api_key)
        url = self.instance_url()
        response, api_key = requestor.request(method=RequestMethod.DELETE, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self
