# Unit tests related to 'Webhook' (https://www.easypost.com/webhooks-guide).

import easypost
import pytest


def test_webhooks(per_run_unique):
    url = 'example.com/{0}'.format(per_run_unique)
    expected_url = 'http://example.com/{0}'.format(per_run_unique)

    # Create a webhook
    webhook = easypost.Webhook.create(url=url)
    assert webhook.id is not None
    assert webhook.mode == "test"
    assert webhook.url == expected_url
    assert webhook.disabled_at is None
    assert isinstance(webhook, easypost.Webhook)

    # Retrieve a webhook
    webhook2 = easypost.Webhook.retrieve(webhook.id)
    assert webhook2.id is not None
    assert webhook2.id == webhook.id

    # Update a webhook (re-enable it)
    webhook3 = webhook.update()
    assert webhook3.id is not None
    assert webhook3.id == webhook.id

    # Index webhooks
    webhooks = easypost.Webhook.all(url=expected_url)
    assert any(wh.id == webhook.id for wh in webhooks['webhooks'])

    # Delete a webhook
    webhook.delete()

    with pytest.raises(easypost.Error) as exception_context:
        easypost.Webhook.retrieve(webhook.id)

    assert exception_context.value.http_status == 404
    assert exception_context.value.message == "The requested resource could not be found."
