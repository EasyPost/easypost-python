# Unit tests related to 'Webhook' (https://www.easypost.com/webhooks-guide).

import unittest
import easypost
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
        try:
            easypost.Webhook.retrieve(webhook.id)
        except easypost.Error as e:
            assert e.http_status == 404
            assert e.message == "The requested resource could not be found."


if __name__ == '__main__':
    unittest.main()
