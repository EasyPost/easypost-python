from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import Requestor
from easypost.resource import AllResource, CreateResource


class Report(AllResource, CreateResource):
    @classmethod
    def create(cls, api_key=None, **params):
        """Create a report."""
        requestor = Requestor(api_key)
        url = f"{cls.class_url()}/{params.get('type')}?"

        if params.get("columns"):
            for column in params.get("columns", []):
                url += f"columns[]={column}&"
            # Delete the columns from the params since it's added in the url query.
            params.pop("columns")

        if params.get("additional_columns"):
            for column in params.get("additional_columns", []):
                url += f"additional_columns[]={column}&"
            # Delete the additional columns from the params since it's added in the url query.
            params.pop("additional_columns")

        response, api_key = requestor.request("post", url, params, False)
        return convert_to_easypost_object(response, api_key)

    @classmethod
    def all(cls, api_key=None, **params):
        """Retrieve all reports."""
        requestor = Requestor(api_key)
        url = "%s/%s" % (cls.class_url(), params["type"])
        response, api_key = requestor.request("get", url, params)
        return convert_to_easypost_object(response, api_key)
