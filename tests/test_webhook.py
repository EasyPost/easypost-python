# Unit tests related to 'Webhook' (https://www.easypost.com/webhooks-guide).

import unittest
import easypost
import pytest

from constants import API_KEY as api_key

easypost.api_key = api_key


class WebhookTests(unittest.TestCase):

    def test_webhooks(self):
        # Create a webhook
        webhook = easypost.Webhook.create(url="example.com")
        assert webhook.id is not None
        assert webhook.mode == "test"
        assert webhook.url == "http://example.com"
        assert webhook.disabled_at is None
        assert type(webhook) == easypost.Webhook

        # Retrieve a webhook
        webhook2 = easypost.Webhook.retrieve(webhook.id)
        assert webhook2.id is not None
        assert webhook2.id == webhook.id

        # Update a webhook (re-enable it)
        webhook3 = webhook.update()
        assert webhook3.id is not None
        assert webhook3.id == webhook.id

        # Index webhooks
        webhooks = easypost.Webhook.all()
        assert webhooks["webhooks"][len(webhooks["webhooks"]) - 1].id == webhook.id

        # Delete a webhook
        webhook.delete()

        with pytest.raises(easypost.Error) as exception_context:
            easypost.Webhook.retrieve(webhook.id)

        assert exception_context.value.http_status == 404
        assert exception_context.value.message == "The requested resource could not be found."
