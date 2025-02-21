import pytest
from easypost.errors import SignatureVerificationError
from easypost.models import Webhook
from easypost.util import validate_webhook


@pytest.mark.vcr()
def test_webhook_create(webhook_url, webhook_secret, webhook_custom_headers, test_client):
    webhook = test_client.webhook.create(
        url=webhook_url,
        webhook_secret=webhook_secret,
        custom_headers=webhook_custom_headers,
    )

    assert isinstance(webhook, Webhook)
    assert str.startswith(webhook.id, "hook_")
    assert webhook.url == webhook_url
    assert webhook.custom_headers[0]["name"] == "test"
    assert webhook.custom_headers[0]["value"] == "header"

    test_client.webhook.delete(
        webhook.id
    )  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_webhook_retrieve(webhook_url, test_client):
    webhook = test_client.webhook.create(url=webhook_url)

    retrieved_webhook = test_client.webhook.retrieve(webhook.id)

    assert isinstance(retrieved_webhook, Webhook)
    assert retrieved_webhook == webhook

    test_client.webhook.delete(
        retrieved_webhook.id
    )  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_webhook_all(page_size, test_client):
    webhooks = test_client.webhook.all(page_size=page_size)

    webhooks_array = webhooks["webhooks"]

    assert len(webhooks_array) <= page_size
    assert all(isinstance(webhook, Webhook) for webhook in webhooks_array)


@pytest.mark.vcr()
def test_webhook_update(webhook_url, webhook_secret, webhook_custom_headers, test_client):
    webhook = test_client.webhook.create(url=webhook_url)
    updated_webhook = test_client.webhook.update(
        webhook.id,
        webhook_secret=webhook_secret,
        custom_headers=webhook_custom_headers,
    )

    assert isinstance(updated_webhook, Webhook)
    assert updated_webhook.custom_headers[0]["name"] == "test"
    assert updated_webhook.custom_headers[0]["value"] == "header"

    test_client.webhook.delete(
        webhook.id
    )  # we are deleting the webhook here so we don't keep sending events to a dead webhook.


@pytest.mark.vcr()
def test_webhook_delete(webhook_url, test_client):
    webhook = test_client.webhook.create(url=webhook_url)

    try:
        test_client.webhook.delete(webhook.id)
    except Exception:
        assert False


def test_validate_webhook(event_bytes, webhook_secret, webhook_hmac_signature):
    headers = {
        "X-Hmac-Signature": webhook_hmac_signature,
    }

    webhook_body = validate_webhook(
        event_body=event_bytes,
        headers=headers,
        webhook_secret=webhook_secret,
    )

    assert webhook_body["description"] == "tracker.updated"
    assert webhook_body["result"]["weight"] == 614.4  # Ensure we convert floats properly


def test_validate_webhook_invalid_secret(event_bytes):
    webhook_secret = "invalid_secret"
    headers = {
        "X-Hmac-Signature": "some-signature",
    }

    with pytest.raises(SignatureVerificationError) as error:
        _ = validate_webhook(
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

    with pytest.raises(SignatureVerificationError) as error:
        _ = validate_webhook(
            event_body=event_bytes,
            headers=headers,
            webhook_secret=webhook_secret,
        )

    assert str(error.value) == "Webhook received does not contain an HMAC signature."
