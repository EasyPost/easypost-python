import pytest

import easypost


@pytest.mark.vcr()
def test_webhook_create(webhook_url):
    webhook = easypost.Webhook.create(url=webhook_url)

    assert isinstance(webhook, easypost.Webhook)
    assert str.startswith(webhook.id, "hook_")
    assert webhook.url == webhook_url

    webhook.delete()  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_webhook_retrieve(webhook_url):
    webhook = easypost.Webhook.create(url=webhook_url)

    retrieved_webhook = easypost.Webhook.retrieve(webhook.id)

    assert isinstance(retrieved_webhook, easypost.Webhook)
    assert retrieved_webhook == webhook

    retrieved_webhook.delete()  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_webhook_all(page_size):
    webhooks = easypost.Webhook.all(page_size=page_size)

    webhooks_array = webhooks["webhooks"]

    assert len(webhooks_array) <= page_size
    assert all(isinstance(webhook, easypost.Webhook) for webhook in webhooks_array)


@pytest.mark.vcr()
@pytest.mark.skip(reason="Cannot be easily tested - requires a disabled webhook.")
def test_webhook_update():
    pass


@pytest.mark.vcr()
def test_webhook_delete(webhook_url):
    webhook = easypost.Webhook.create(url=webhook_url)

    response = webhook.delete()

    # This endpoint/method does not return anything, just make sure the request doesn't fail
    assert isinstance(response, easypost.Webhook)
