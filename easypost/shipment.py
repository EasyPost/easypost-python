from easypost.error import Error
from easypost.requestor import Requestor
from easypost.resource import AllResource, CreateResource


class Shipment(AllResource, CreateResource):
    def regenerate_rates(self):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "rerate")
        response, api_key = requestor.request("post", url)
        self.refresh_from(response, api_key)
        return self

    def get_smartrates(self):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "smartrate")
        response, api_key = requestor.request("get", url)
        return response.get("result", [])

    def buy(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "buy")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self

    def refund(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "refund")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self

    def insure(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "insure")
        response, api_key = requestor.request("post", url, params)
        self.refresh_from(response, api_key)
        return self

    def label(self, **params):
        requestor = Requestor(self._api_key)
        url = "%s/%s" % (self.instance_url(), "label")
        response, api_key = requestor.request("get", url, params)
        self.refresh_from(response, api_key)
        return self

    def lowest_rate(self, carriers=None, services=None):
        carriers = carriers or []
        services = services or []
        lowest_rate = None

        try:
            carriers = carriers.split(",")
        except AttributeError:
            pass
        carriers = [c.lower() for c in carriers]

        try:
            services = services.split(",")
        except AttributeError:
            pass
        services = [service.lower() for service in services]

        for rate in self.rates:
            if len(carriers) > 0 and rate.carrier.lower() not in carriers:
                continue

            if len(services) > 0 and rate.service.lower() not in services:
                continue

            if lowest_rate is None or float(rate.rate) < float(lowest_rate.rate):
                lowest_rate = rate

        if lowest_rate is None:
            raise Error("No rates found.")

        return lowest_rate
