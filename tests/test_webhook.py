import pytest
from easypost.errors import SignatureVerificationError
from easypost.models import Webhook
from easypost.util import validate_webhook


@pytest.mark.vcr()
def test_webhook_create(webhook_url, test_client):
    webhook = test_client.webhook.create(url=webhook_url)

    assert isinstance(webhook, Webhook)
    assert str.startswith(webhook.id, "hook_")
    assert webhook.url == webhook_url

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
def test_webhook_update(webhook_url, test_client):
    webhook = test_client.webhook.create(url=webhook_url)
    test_client.webhook.update(webhook.id)

    assert isinstance(webhook, Webhook)

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


def test_validate_webhook(event_bytes):
    webhook_secret = "sécret"
    expected_hmac_signature = "hmac-sha256-hex=e93977c8ccb20363d51a62b3fe1fc402b7829be1152da9e88cf9e8d07115a46b"
    headers = {
        "X-Hmac-Signature": expected_hmac_signature,
    }

    webhook_body = validate_webhook(
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
