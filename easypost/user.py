from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import Requestor
from easypost.resource import CreateResource, DeleteResource, UpdateResource


class User(CreateResource, UpdateResource, DeleteResource):
    @classmethod
    def create(cls, api_key=None, **params):
        requestor = Requestor(api_key)
        url = cls.class_url()
        wrapped_params = {cls.snakecase_name(): params}
        response, api_key = requestor.request("post", url, wrapped_params, False)
        return convert_to_easypost_object(response, api_key)

    @classmethod
    def retrieve(cls, easypost_id="", api_key=None, **params):
        try:
            easypost_id = easypost_id["id"]
        except (KeyError, TypeError):
            pass

        if easypost_id == "":
            requestor = Requestor(api_key)
            response, api_key = requestor.request("get", cls.class_url())
            return convert_to_easypost_object(response, api_key)
        else:
            instance = cls(easypost_id, api_key, **params)
            instance.refresh()
            return instance

    @classmethod
    def retrieve_me(cls, api_key=None, **params):
        requestor = Requestor(api_key)
        response, api_key = requestor.request("get", cls.class_url())
        return convert_to_easypost_object(response, api_key)

    @classmethod
    def all_api_keys(cls, api_key=None):
        requestor = Requestor(api_key)
        url = "/api_keys"
        response, api_key = requestor.request("get", url)
        return convert_to_easypost_object(response, api_key)

    def api_keys(self):
        api_keys = self.all_api_keys()

        if api_keys.id == self.id:
            my_api_keys = api_keys.keys
        else:
            for child in api_keys.children:
                if child.id == self.id:
                    my_api_keys = child.keys
                    break

        return my_api_keys

    def update_brand(self, api_key=None, **params):
        requestor = Requestor(api_key)
        response, api_key = requestor.request("put", self.instance_url() + "/brand", params)
        return convert_to_easypost_object(response, api_key)
