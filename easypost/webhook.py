import hashlib
import hmac
import json
import unicodedata
from typing import (
    Any,
    Dict,
)

from easypost.error import Error
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.resource import (
    AllResource,
    CreateResource,
    DeleteResource,
)


class Webhook(AllResource, CreateResource, DeleteResource):
    def update(self, **params) -> "Webhook":
        """Update a webhook."""
        requestor = Requestor(local_api_key=self._api_key)
        url = self.instance_url()
        response, api_key = requestor.request(method=RequestMethod.PATCH, url=url, params=params)
        self.refresh_from(values=response, api_key=api_key)
        return self

    @staticmethod
    def validate_webhook(event_body: bytes, headers: Dict[str, Any], webhook_secret: str) -> Dict[str, Any]:
        """Validate a webhook by comparing the HMAC signature header sent from EasyPost to your shared secret.
        If the signatures do not match, an error will be raised signifying the webhook either did not originate
        from EasyPost or the secrets do not match. If the signatures do match, the `event_body` will be returned
        as JSON.
        """
        easypost_hmac_signature = headers.get("X-Hmac-Signature")

        if easypost_hmac_signature:
            normalized_secret = unicodedata.normalize("NFKD", webhook_secret)
            encoded_secret = bytes(normalized_secret, "utf8")

            expected_signature = hmac.new(
                key=encoded_secret,
                msg=event_body,
                digestmod=hashlib.sha256,
            )

            digest = "hmac-sha256-hex=" + expected_signature.hexdigest()

            if hmac.compare_digest(digest, easypost_hmac_signature):
                webhook_body = json.loads(event_body)
            else:
                raise Error(
                    message="Webhook received did not originate from EasyPost or had a webhook secret mismatch."
                )
        else:
            raise Error(message="Webhook received does not contain an HMAC signature.")

        return webhook_body
