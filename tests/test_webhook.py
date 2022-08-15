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
def test_webhook_update(webhook_url):
    webhook = easypost.Webhook.create(url=webhook_url)
    webhook.update()

    assert isinstance(webhook, easypost.Webhook)

    webhook.delete()  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_webhook_delete(webhook_url):
    webhook = easypost.Webhook.create(url=webhook_url)

    response = webhook.delete()

    # This endpoint/method does not return anything, just make sure the request doesn't fail
    assert isinstance(response, easypost.Webhook)


def test_validate_webhook(event_bytes):
    webhook_secret = "sécret"
    expected_hmac_signature = "hmac-sha256-hex=e93977c8ccb20363d51a62b3fe1fc402b7829be1152da9e88cf9e8d07115a46b"
    headers = {
        "X-Hmac-Signature": expected_hmac_signature,
    }

    webhook_body = easypost.Webhook.validate_webhook(
        event_body=event_bytes,
        headers=headers,
        webhook_secret=webhook_secret,
    )

    assert webhook_body["description"] == "batch.created"


def test_validate_webhook_invalid_secret(event_bytes):
    webhook_secret = "invalid_secret"
    headers = {
        "X-Hmac-Signature": "some-signature",
    }

    with pytest.raises(easypost.Error) as error:
        _ = easypost.Webhook.validate_webhook(
            event_body=event_bytes,
            headers=headers,
            webhook_secret=webhook_secret,
        )

    assert str(error.value) == "Webhook received did not originate from EasyPost or had a webhook secret mismatch."


def test_validate_webhook_missing_secret(event_bytes):
    webhook_secret = "123"
    headers = {
        "some-header": "some-value",
    }

    with pytest.raises(easypost.Error) as error:
        _ = easypost.Webhook.validate_webhook(
            event_body=event_bytes,
            headers=headers,
            webhook_secret=webhook_secret,
        )

    assert str(error.value) == "Webhook received does not contain an HMAC signature."
